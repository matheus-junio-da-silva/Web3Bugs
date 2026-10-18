#!/usr/bin/env python3
"""HELIX / Project 15 GHO Core: reproduce a historical-source CVL catalog.
Runs in a real GitHub Actions checkout, never edits Project 2 or source contracts.
"""
import collections
import csv
import hashlib
import io
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"Web3Bugs-certora"
ARCHIVE=Path("/tmp/p15-gho-propertygpt/certora_projects/gho-core")
REVIEW=Path("/tmp/p15-gho-reviewed")
PDF_URL="https://certora.cdn.prismic.io/certora/a227c693-7aa3-471f-a7b2-7148c06a2110_Aave_Gho_Formal_Verification_Report.pdf"
REVIEW_COMMIT="ce49fb0c94cfebf0159222ceb288e4f9a55d305f"
SOURCE_COMMIT="687f654c679ed45ab127b7949e2a29c8f5e491b9"
SPEC_FILES=["VariableDebtToken.spec","erc20.spec","flashMinter.spec","ghoAToken.spec",
 "ghoDiscountRateStrategy.spec","ghoToken.spec","ghoVariableDebtToken.spec","set.spec","summarizations.spec"]
COUNTS={"VariableDebtToken.spec":22,"erc20.spec":0,"flashMinter.spec":6,
 "ghoAToken.spec":7,"ghoDiscountRateStrategy.spec":1,"ghoToken.spec":28,
 "ghoVariableDebtToken.spec":25,"set.spec":27,"summarizations.spec":0}
SOL_TARGET={
 "VariableDebtToken.spec":"GhoVariableDebtToken",
 "flashMinter.spec":"GhoFlashMinter",
 "ghoAToken.spec":"GhoAToken",
 "ghoDiscountRateStrategy.spec":"GhoDiscountRateStrategy",
 "ghoToken.spec":"GhoToken",
 "ghoVariableDebtToken.spec":"GhoVariableDebtToken",
 "set.spec":"GhoToken",
}
SOL_FILES={
 "GhoVariableDebtToken":["facilitators/aave/tokens/GhoVariableDebtToken.sol",
                          "facilitators/aave/tokens/base/ScaledBalanceTokenBase.sol"],
 "GhoFlashMinter":["facilitators/flashMinter/GhoFlashMinter.sol","gho/GhoToken.sol"],
 "GhoAToken":["facilitators/aave/tokens/GhoAToken.sol","gho/GhoToken.sol"],
 "GhoDiscountRateStrategy":["facilitators/aave/interestStrategy/GhoDiscountRateStrategy.sol"],
 "GhoToken":["gho/GhoToken.sol","gho/ERC20.sol"],
}
# Report: individual names with explicit checked status, associated with the
# corresponding concrete target. Never assign report results to unlisted rules,
# diagnostic set-spec probes, or a similarly named non-identical property.
REPORTED={
 "GhoVariableDebtToken":set("""discountCantExceed100Percent disallowedFunctionalities
 nonMintFunctionCantIncreaseBalance nonMintFunctionCantIncreaseScaledBalance
 debtTokenIsNotTransferable onlyCertainFunctionsCanModifyScaledBalance
 userAccumulatedDebtInterestWontDecrease userCantNullifyItsDebt
 integrityOfMint_updateDiscountRate integrityOfMint_updateIndex
 integrityOfMint_userIsolation onlyMintForUserCanIncreaseUsersBalance
 integrityOfBurn_updateDiscountRate integrityOfBurn_updateIndex integrityOfBurn_fixedIndex
 burnZeroDoesntChangeBalance integrityOfBurn_fullRepay_concrete integrityOfBurn_userIsolation
 integrityOfUpdateDiscountDistribution_updateIndex
 integrityOfUpdateDiscountDistribution_userIsolation
 integrityOfRebalanceUserDiscountPercent_updateDiscountRate
 integrityOfRebalanceUserDiscountPercent_updateIndex
 integrityOfRebalanceUserDiscountPercent_userIsolation
 integrityOfBalanceOf_fullDiscount integrityOfBalanceOf_noDiscount
 integrityOfBalanceOf_zeroScaledBalance""".split()),
 "GhoDiscountRateStrategy":{"limitOnDiscountRate"},
 "GhoToken":set("""inv_balanceOf_leq_totalSupply sumAllBalance_eq_totalSupply
 length_leq_max_uint160 total_supply_eq_sumAllLevel sumAllLevel_eq_sumAllBalance
 inv_valid_capacity inv_valid_level address_in_set_values_iff_in_set_indexes
 addr_in_set_iff_in_map level_leq_capacity facilitator_in_list_after_setFacilitatorBucketCapacity
 getFacilitatorBucketCapacity_after_setFacilitatorBucketCapacity
 facilitator_in_list_after_addFacilitator address_not_in_list_after_removeFacilitator
 mint_after_burn burn_after_mint level_unchanged_after_mint_followed_by_burn
 level_after_mint level_after_burn facilitator_in_list_after_mint_and_burn
 balance_after_mint balance_after_burn mintLimitedByFacilitatorRemainingCapacity
 burnLimitedByFacilitatorLevel""".split()),
 "GhoAToken":set("""noMint noBurn noTransfer transferUnderlyingToCantExceedCapacity
 totalSupplyAlwaysZero userBalanceAlwaysZero
 level_does_not_decrease_after_transferUnderlyingTo_followed_by_handleRepayment""".split()),
 "GhoFlashMinter":set("""balanceOfFlashMinterGrows integrityOfTreasurySet
 integrityOfFeeSet availableLiquidityDoesntChange integrityOfDistributeFeesToTreasury
 feeSimulationEqualsActualFee""".split())
}
# The PDF's VIOLATED onlyRebalanceCanUpdateUserDiscountRate is not an active
# declaration in this archived source. The timed-out integrityOfMint_cantDecreaseInterestWithMint
# is not an active declaration either; never insert either into a .spec.
REPORT_MISMATCHES={"onlyRebalanceCanUpdateUserDiscountRate":"VIOLATED in PDF, absent from archived active CVL",
 "integrityOfMint_cantDecreaseInterestWithMint":"TIMEOUT in PDF, absent from archived active CVL",
 "integrityOfUpdateDiscountDistribution_discountRate":"VERIFIED in PDF, absent from archived active CVL",
 "OnlyFacilitatorManagerAlterFacilitatorExistence":"VERIFIED in PDF, absent from archived active CVL",
 "OnlyBucketManagerCanChangeCapacity":"VERIFIED in PDF, absent from archived active CVL"}
HDR=["Project ID","Status","Example ID","Bug Label","Property","Result",
 "Detection Outcome","Target Contract","Spec","Code","Documentation",
 "Incomplete Reason","Original Spec","Original Spec Lines",
 "Original Contract","Original Contract Lines","Detection Intent"]

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git_blob(path):
    return subprocess.check_output(["git","hash-object",str(path)]).decode().strip()

def report_contains(text,name):
    normalized=re.sub(r"\s+","",text).casefold()
    return name.casefold() in normalized

def properties(text):
    """Find top-level source declarations; retain property bytes literally."""
    rx=re.compile(r"(?m)^[ \t]*(rule|invariant)\s+([A-Za-z_]\w*)\b")
    matches=list(rx.finditer(text))
    segments=[]
    for i,m in enumerate(matches):
        # Stop at next declaration, or a ghost/hook/function/definition following
        # this property. Interspersed original comments are source-preserved.
        next_start=matches[i+1].start() if i+1<len(matches) else len(text)
        other=re.search(r"(?m)^[ \t]*(?:ghost|hook|definition|function|methods|import|using)\b",
                        text[m.end():next_start])
        if other:next_start=m.end()+other.start()
        seg=text[m.start():next_start].rstrip("\r\n")
        start_line=text.count("\n",0,m.start())+1
        end_line=start_line+seg.count("\n")
        segments.append(dict(kind=m.group(1),name=m.group(2),
             body=seg,first=start_line,last=end_line,begin=m.start(),end=next_start))
    return segments

def trim_properties(text,decls):
    ranges=sorted((d["begin"],d["end"]) for d in decls)
    cursor=0
    pieces=[]
    for a,b in ranges:
        if a>cursor:pieces.append(text[cursor:a])
        cursor=b
    if cursor<len(text):pieces.append(text[cursor:])
    return "".join(pieces)

def imported_closure(spec_name,sources,seen=None):
    seen=set() if seen is None else seen
    if spec_name in seen:return []
    seen.add(spec_name)
    src=sources[spec_name]
    imports=re.findall(r'(?m)^[ \t]*import[ \t]+"([^"]+)"',src)
    output=[]
    for dep in imports:
        assert dep in sources, (spec_name,"missing imported spec",dep)
        output+=imported_closure(dep,sources,seen)
    output.append(spec_name)
    return output

def solidity_region(lines,initial):
    # Find whole function or storage region with braces retained verbatim.
    i=initial
    while i<len(lines) and "{" not in lines[i] and ";" not in lines[i]:i+=1
    if i>=len(lines):return initial
    if ";" in "".join(lines[initial:i+1]) and "{" not in "".join(lines[initial:i+1]):
        return i
    depth=0;opened=False
    for k in range(initial,i+1):
        for c in lines[k]:
            if c=="{":depth+=1;opened=True
            elif c=="}":depth-=1
    if opened and depth==0:return i
    for k in range(i+1,len(lines)):
        for c in lines[k]:
            if c=="{":depth+=1
            elif c=="}":depth-=1
        if opened and depth<=0:return k
    return min(i+30,len(lines)-1)

def relevant_solidity(spec_name,property_body,name,target):
    token_set=set(re.findall(r"[A-Za-z_]\w*",property_body))
    token_set|={name}
    # Storage and function names linked to the particular property, not a generic
    # whole-contract paste. Retain bounded concrete excerpts and exact line ranges.
    preferred={
      "GhoToken":["_facilitators","_facilitatorsList","balanceOf","totalSupply","mint","burn",
          "addFacilitator","removeFacilitator","setFacilitatorBucketCapacity"],
      "GhoAToken":["_ghoToken","transferUnderlyingTo","handleRepayment","mint","burn"],
      "GhoFlashMinter":["_ghoToken","_fee","_ghoTreasury","flashLoan","flashFee",
          "maxFlashLoan","distributeFees","updateFee","updateGhoTreasury"],
      "GhoVariableDebtToken":["_ghoUserState","_userState","_balances","_totalSupply",
         "mint","burn","balanceOf","scaledBalanceOf","updateDiscountDistribution",
         "rebalanceUserDiscountPercent"],
      "GhoDiscountRateStrategy":["calculateDiscountRate","DISCOUNT_RATE",
         "GHO_DISCOUNTED_PER_DISCOUNT_TOKEN"],
    }
    wanted=set(x for x in preferred[target] if x in token_set)
    if not wanted:
        wanted=set([x for x in preferred[target] if x.lower() in name.lower()])
    if not wanted:
        wanted=set(preferred[target][:3])
    sections=[];pathlist=[];linelist=[];mechanisms=[]
    for rel in SOL_FILES[target]:
        path=ARCHIVE/rel
        lines=path.read_text().splitlines(keepends=True)
        selected=[]
        for index,line in enumerate(lines):
            match=re.search(r"^\s*(?:function|constructor|modifier)\s+([A-Za-z_]\w*)",line)
            if match and match.group(1) in wanted:
                selected.append((index,solidity_region(lines,index),match.group(1)))
            if any(re.search(r"\b"+re.escape(tok)+r"\b",line) for tok in wanted):
                if re.search(r"^\s*(?:mapping\s*\(|(?:uint\d*|address|bool|bytes\d*|string)\s+(?:public|private|internal|immutable|constant|\s)*\b)",line):
                    selected.append((index,solidity_region(lines,index),"storage"))
        # For a target whose property refers only to a getter, get its concrete
        # implementation or at least actual storage declaration, never invent it.
        if not selected and rel==SOL_FILES[target][0]:
            for k,line in enumerate(lines):
                if re.search(r"\bcontract\s+\w+|\bmapping\s*\(",line):
                    selected.append((k,k,"contract/state context"))
                    if len(selected)>=3:break
        used=[]
        for a,b,mechanism in sorted(selected):
            if any(a>=x and b<=y for x,y in used):continue
            if len(sections)>=12:break
            used.append((a,b))
            lo=a+1;hi=b+1
            slice_text="".join(lines[a:b+1])
            sections.append("// Original Solidity: contracts/15/"+rel+
                            " lines "+str(lo)+"-"+str(hi)+"; "+mechanism+"\n"+slice_text.rstrip("\r\n")+"\n")
            pathlist.append("contracts/15/"+rel)
            linelist.append(str(lo)+"-"+str(hi))
            mechanisms.append(mechanism)
    assert sections,(spec_name,name,"No local Solidity excerpt")
    paths=[]; lineby=[]
    for p,li in zip(pathlist,linelist):
        if p not in paths:paths.append(p)
    for p in paths:
        lineby.append(";".join(x for q,x in zip(pathlist,linelist) if q==p))
    return "\n".join(sections),"; ".join(paths)," | ".join(lineby),list(dict.fromkeys(mechanisms))

def tech_label(name,body,source):
    low=name.lower()
    if low.startswith("cover_") or ("should_fail" in low) or low.startswith("whochange") or low.startswith("balanceofchange"):
        return "UNMAPPED","Diagnostic/reachability or mutation exploration without a uniquely defensible security oracle."
    if low.startswith("api_") and source=="set.spec":
        return "S2-3","Checks set membership or index identity after an add/remove operation."
    if "unique" in low or "inverse" in low or "in_set" in low or "not_in_list" in low or "addressset" in low:
        return "S2-3","Detects mismatch/duplication between index, address, and set membership representations."
    if "facilitator" in low and ("capacity" in low or "level" in low):
        return "S3-2","Detects an incorrect facilitator level or capacity state transition."
    if "disallowed" in low or "nottransferable" in low or low in ("nomint","noburn","notransfer"):
        return "S5-2","Checks that a disallowed external operation cannot succeed."
    if "treasuryset" in low or "feeset" in low or "updateindex" in low or "updatediscountrate" in low:
        return "S3-2","Checks the specified configuration/index update and prevents an incorrect state transition."
    if "limiton" in low or "rate" in low and ("discount" in low or "balanceof" in low):
        return "S6-2","Checks that computed return values stay within the specified discount-rate semantics."
    if "balance" in low or "supply" in low or "mint" in low or "burn" in low or "debt" in low or "fee" in low or "liquidity" in low or "discount" in low or "capacity" in low or "level" in low:
        return "S6-4","Detects an accounting/conservation or amount-transition discrepancy."
    if source=="set.spec":return "UNMAPPED","Generic set implementation probe; no project-specific security intent is independently established."
    return "UNMAPPED","No defensible unique Web3Bugs bug class established by the executable assertion."

def statement(body,kind):
    if kind=="invariant":
        m=re.search(r"(?s)\binvariant\s+\w+[^\n]*\n(.*)",body)
        if m:return re.sub(r"\s+"," ",m.group(1)).strip()[:400]
        return re.sub(r"\s+"," ",body).strip()[:400]
    chunks=re.findall(r"(?s)\bassert\s*(?:\([^;]*?\)|[^;]+);",body)
    if not chunks:
        # CVL may have assert on expression without semicolon
        chunks=re.findall(r"(?m)^[ \t]*assert[^\n]*",body)
    return " ".join(re.sub(r"\s+"," ",c).strip() for c in chunks[:5])[:750] or "No explicit assert; inspect the literal CVL rule and its method/revert semantics."

def add_csv(path,rows,fields):
    original=path.read_bytes()
    eol="\r\n" if b"\r\n" in original else "\n"
    stream=io.StringIO(newline="")
    writer=csv.DictWriter(stream,fieldnames=fields,lineterminator=eol)
    writer.writerows(rows)
    path.write_bytes(original+(b"" if original.endswith((b"\r",b"\n")) else eol.encode())+stream.getvalue().encode())

def run():
    assert ARCHIVE.is_dir(),ARCHIVE
    assert REVIEW.is_dir(),REVIEW
    assert not (DATA/"contracts/15").exists(),"Refuse to overwrite Project 15"
    assert not (DATA/"results/spec/incomplete/15").exists(),"Refuse to overwrite index"
    texts={name:(ARCHIVE/name).read_text() for name in SPEC_FILES}
    props={name:properties(texts[name]) for name in SPEC_FILES}
    assert {x:len(v) for x,v in props.items()}==COUNTS,[(k,len(v)) for k,v in props.items()]
    assert sum(COUNTS.values())==116
    src_files=[p for p in ARCHIVE.rglob("*.sol")]
    assert len(src_files)==22,len(src_files)
    assert not list(ARCHIVE.rglob("*.pdf")), "Unexpected report in archived source"
    snapshot=DATA/"contracts/15"
    shutil.copytree(ARCHIVE,snapshot)
    # Pin and compare the precise original contract byte-content against the
    # report's historical reviewed commit, not against current upstream main.
    checked=[]
    for p in src_files:
        rel=p.relative_to(ARCHIVE)
        up=REVIEW/"src/contracts"/rel
        assert up.is_file(),("Reviewed commit missing",rel)
        assert git_blob(p)==git_blob(up),("Solidity version mismatch",rel)
        checked.append((str(rel),git_blob(p)))
    spec_drift=[]
    for name in SPEC_FILES:
        up=REVIEW/"certora/specs"/name
        assert up.is_file(),("Reviewed commit missing spec",name)
        if git_blob(ARCHIVE/name)!=git_blob(up):
            spec_drift.append(name)
    assert spec_drift==["ghoDiscountRateStrategy.spec"],spec_drift
    a=next(d for d in props["ghoDiscountRateStrategy.spec"] if d["name"]=="limitOnDiscountRate")
    b=next(d for d in properties((REVIEW/"certora/specs/ghoDiscountRateStrategy.spec").read_text()) if d["name"]=="limitOnDiscountRate")
    assert a["body"].strip()==b["body"].strip(),"Discount-rule body mismatch"
    resource=DATA/"resources/15"
    resource.mkdir(parents=True)
    pdf=Path("/tmp/p15-gho-report.pdf")
    assert pdf.is_file() and pdf.stat().st_size>50000,"Official historical PDF download missing"
    shutil.copy2(pdf,resource/"Aave_Gho_Formal_Verification_Report.pdf")
    layout=subprocess.run(["pdftotext","-layout",str(pdf),"-"],capture_output=True,text=True,check=True).stdout
    assert "GhoToken" in layout and "GhoFlashMinter" in layout and "GhoVariableDebtToken" in layout
    report=(DATA/"reports/15.md")
    report.write_text("---\ntitle: Certora AAVE GHO Core Formal Verification Report\n"
       "slug: aave-gho-core\nsponsor: Aave\ndate: 2023-03\ncontest: 15\n---\n\n"
       "# Historical report PDF text-layer transcript (layout-preserving)\n\n"
       "Official report URL: "+PDF_URL+"\nPDF SHA256: "+sha256(pdf)+"\n"
       "Reviewed target commit: "+REVIEW_COMMIT+"\n\n"
       "The original 13-page PDF in resources/15 is authoritative for tables, glyphs and page layout.\n\n"
       "~~~text\n"+layout.replace("~~~","~ ~ ~")+"\n~~~\n")
    # No attributions to source-absent report rules; even matching names must
    # occur in the actual PDF and in the verified historical source version.
    for target,names in REPORTED.items():
        for n in names:
            assert report_contains(layout,n),("PDF report does not mention listed property",target,n)
    dest=DATA/"results/spec/incomplete/15"
    dest.mkdir(parents=True)
    rows=[]
    review=[];unverified=[];failures=[]
    idn=0
    for spec_name in SPEC_FILES:
        if spec_name not in SOL_TARGET:continue
        target=SOL_TARGET[spec_name]
        for prop in props[spec_name]:
            idn+=1
            name=prop["name"];body=prop["body"];kind=prop["kind"]
            closure=imported_closure(spec_name,texts)
            prelude=[]
            for dep in closure:
                original=texts[dep]
                available=trim_properties(original,props[dep])
                available=re.sub(r'(?m)^[ \t]*import[ \t]+"[^"]+"[ \t]*\n',"",available)
                prelude.append("// Original CVL non-property helpers from contracts/15/"+dep+
                    "\n"+available.rstrip("\r\n")+"\n")
            extras=[]
            # Recur on requireInvariant, copying the original declaration when used.
            req=set(re.findall(r"\brequireInvariant\s+([A-Za-z_]\w*)",body))
            pulled=set()
            while req:
                required=req.pop()
                if required in pulled:continue
                pulled.add(required)
                other=[(file,d) for file in closure for d in props[file]
                       if d["kind"]=="invariant" and d["name"]==required]
                if not other:continue
                file,d=other[0]
                extras.append("// Required original invariant: contracts/15/"+file+
                              " lines "+str(d["first"])+"-"+str(d["last"])+"\n"+d["body"]+"\n")
                req|=set(re.findall(r"\brequireInvariant\s+([A-Za-z_]\w*)",d["body"]))-pulled
            path=dest/f"{idn}.spec"
            content="// HELIX Project 15 historical CVL extraction\n"
            content+="// Source contracts/15/"+spec_name+" property lines "+str(prop["first"])+"-"+str(prop["last"])+"\n"
            content+="// Historic syntax unchanged; dependency-incomplete, no CVL2 migration\n\n"
            content+="\n".join(prelude)+"\n".join(extras)+"\n"
            content+="// Exact literal original property follows\n"+body+"\n"
            path.write_text(content)
            assert body in path.read_text(),(spec_name,name,"Literal property not preserved")
            sol,orig_paths,orig_lines,mechanisms=relevant_solidity(spec_name,body,name,target)
            (dest/f"{idn}.sol").write_text(sol)
            # The preserved 22 local Solidity files match the reviewed commit,
            # but imports from external packages and verification harnesses do not
            # exist in the PropertyGPT snapshot. Name the specific constraints.
            aliases=re.findall(r"(?m)^\s*using\s+(\w+)\s+as\s+(\w+)",texts[spec_name])
            missing=[]
            local_names={p.stem for p in src_files}
            for a,alias in aliases:
                if a not in local_names:
                    missing.append("CVL using alias "+alias+" target "+a+" has no implementation in the source snapshot")
            if spec_name=="ghoAToken.spec":
                missing.append("GhoTokenHarness named in using declaration is absent")
            if spec_name=="flashMinter.spec":
                missing.append("MockFlashBorrower and any mock callback/flash borrower harness are absent")
            if spec_name=="VariableDebtToken.spec":
                missing.append("Generic VariableDebtToken spec is imported into GhoVariableDebtToken, but its stand-alone run target is undocumented")
            if spec_name=="set.spec":
                missing.append("Generic set probe spec is imported by ghoToken.spec; no independent set harness/run target is archived")
            missing.append("Unvendored historical Solidity library imports (Aave V3/OpenZeppelin and other upstream packages) and original solc/link Prover configuration")
            missing=list(dict.fromkeys(missing))
            label,intent=tech_label(name,body,spec_name)
            same_blob=git_blob(ARCHIVE/spec_name)==git_blob(REVIEW/"certora/specs"/spec_name)
            reviewed=(same_blob or spec_name=="ghoDiscountRateStrategy.spec")
            matched=reviewed and name in REPORTED.get(target,set()) and report_contains(layout,name)
            result="VERIFIED" if matched else "NOT_STATED"
            outcome="NO_FINDING" if matched else "NOT_STATED"
            # No user-requested finding is fabricated: report's actual VIOLATED
            # property is absent from this archived snapshot.
            assertion=statement(body,kind)
            (dest/f"{idn}.txt").write_text(
                "INCOMPLETE HISTORICAL SOURCE DEPENDENCIES\n"+
                "Property: "+name+"\nOriginal Spec: contracts/15/"+spec_name+
                " lines "+str(prop["first"])+"-"+str(prop["last"])+"\nTarget: "+target+"\n\n"+
                "\n".join("- "+x for x in missing)+"\n\n"+
                "A CVL methods declaration is not a missing Solidity method implementation. "
                "External package versions, harness behavior, deployment linkages and the "
                "historical Prover run cannot be reconstructed soundly from this snapshot. "
                "The preserved source era is not modernized to CVL2. "
                "Historical report status "+result+" must not be read as a fresh proof.\n")
            refs=[f"contracts/15/{spec_name}:{prop['first']}-{prop['last']}"]
            refs += [f"contracts/15/{d}" for d in closure if d!=spec_name]
            status_note=("An exact source property name was found in the official PDF, and its "
                         "rule body matches the reviewed commit's spec (the lone shortened "
                         "discount spec retains this same rule)." if matched else
                         "No individually attributable verified/violated outcome for this exact "
                         "active source instance and target; NOT_STATED rather than inferred.")
            report_identity="report ce49fb0; archived 22/22 Solidity blobs equal and 8/9 source specs equal"
            if spec_name=="ghoDiscountRateStrategy.spec":
                report_identity+="; archived spec has four fewer active rules but this rule body is identical"
            doc=f"""# Example {idn} — {name}

## Status
**incomplete** — concrete missing historical source/configuration recorded in {idn}.txt.
Not a CVL1/CVL2 migration decision.

## Historical result and audit outcome
- Result: **{result}**
- Detection Outcome: **{outcome}**
- Exact report evidence: {status_note}
- Historical identity: {report_identity}
- Original report: reports/15.md; original PDF resources/15/Aave_Gho_Formal_Verification_Report.pdf; official URL {PDF_URL}.

## Target and source
- Target Contract: **{target}** (for helper specs, inferred from its import by the target spec; exact independent run configuration missing).
- Original property: contracts/15/{spec_name}, {kind} lines {prop['first']}-{prop['last']}.
- Imported CVL dependencies traversed: {', '.join(closure)}.
- Required invariant dependencies: {', '.join(sorted(pulled)) if pulled else 'none in executable property'}.
- Original Solidity: {orig_paths}.
- Original Solidity ranges: {orig_lines}.

## Motivation and technical classification
- Bug Label: **{label}**.
- Detection intent: {intent}
- This is a taxonomy for the executable predicate, **not** a classification of the report's distinct historical findings.

## Reconstructed verification methodology
1. Consider the symbolic input/state and the CVL requires, summaries, ghost and hook assumptions in the literal rule.
2. Exercise only calls actually encoded by this property, using the named {target} target and imported helpers.
3. Compare the state/return values in the exact CVL predicate below, without substituting explanatory PDF formulae or differently named rules.
4. A counterexample requires a satisfiable trace satisfying its preconditions for which this assertion becomes false (or its explicit revert/no-revert expectation fails). A statement filtered out by the original CVL is **not** checked.

### What specifically falsifies the assertion
~~~cvl
{assertion}
~~~

For an invariant, the quoted predicate must hold in each modeled preserved state; for a rule, the executable assertions govern. Any source assumption, filter or stub limits this claim.

## Why the Solidity excerpt is relevant
The source slices identify concrete {target} functions/storage used to compute the CVL-observed values, including **{', '.join(mechanisms)}**. They come from **{orig_paths}** at original lines **{orig_lines}**. The excerpt is a literal contextual slice from the archived Solidity, not a replacement compilable contract; no helper behavior is invented. Its state transitions or getters are the implementation paths against which the predicate above is compared. In particular, do not infer changes to a user's debt, facilitator level, fee or discount from a name alone.

## Missing dependency and soundness limitations
{chr(10).join('- '+s for s in missing)}

The report assumes Aave V3 Pool works as intended, setter-initialized links already exist, loops are unrolled to two iterations, and WAD/RAY/BPS formats are respected. No result is extrapolated to other target, contract version, nonmatching active rule, or external call behavior. The original PDF discusses additional properties and manual findings that are not automatically assigned here.

## Semantic second review
- Executable behavior and falsifying condition: **{assertion}**.
- Technical label: **{label}**, justified only by the actual predicate.
- Target: **{target}**, with import/run qualifications above.
- Report linkage: **{result} / {outcome}**; {status_note}
"""
            (dest/f"{idn}.md").write_text("\n".join(x.rstrip() for x in doc.splitlines())+"\n")
            row={"Project ID":"15","Status":"incomplete","Example ID":str(idn),
                "Bug Label":label,"Property":name,"Result":result,
                "Detection Outcome":outcome,"Target Contract":target,
                "Spec":f"results/spec/incomplete/15/{idn}.spec",
                "Code":f"results/spec/incomplete/15/{idn}.sol",
                "Documentation":f"results/spec/incomplete/15/{idn}.md",
                "Incomplete Reason":f"results/spec/incomplete/15/{idn}.txt",
                "Original Spec":f"contracts/15/{spec_name}",
                "Original Spec Lines":str(prop["first"])+"-"+str(prop["last"]),
                "Original Contract":orig_paths,
                "Original Contract Lines":orig_lines,
                "Detection Intent":intent}
            rows.append(row)
            review.append((idn,spec_name,name,target,result,label))
            if not matched:unverified.append((spec_name,name))
    assert idn==116,(idn,"Wrong active property coverage")
    assert len(rows)==116
    csvfile=DATA/"results/spec/spec_buglabel.csv"
    old=list(csv.DictReader(io.StringIO(csvfile.read_bytes().decode(),newline="")))
    assert not any(x["Project ID"]=="15" for x in old)
    add_csv(csvfile,rows,HDR)
    contest=DATA/"results/contests.csv"
    orig=contest.read_bytes()
    assert not re.search(rb"(?m)^15,",orig)
    eol=b"\r\n" if b"\r\n" in orig else b"\n"
    contest.write_bytes(orig+(b"" if orig.endswith((b"\r",b"\n")) else eol)+
        b"15,AAVE GHO Core,Stablecoin,-,-,2023-02,-,-"+eol)
    attrs=DATA/".gitattributes"
    attrs.write_text(attrs.read_text().rstrip("\n")+
       "\n\n# HELIX Project 15 historical source: retain original whitespace bytes.\n"+
       "contracts/15/** -whitespace\n"+
       "results/spec/incomplete/15/*.spec -whitespace\n"+
       "results/spec/incomplete/15/*.sol -whitespace\n"+
       "reports/15.md -whitespace\n")
    # Provenance and caveats: source-era report matches 22 Solidity snapshots.
    metadata=["# HELIX — Project 15 / AAVE GHO Core","",
      "## Provenance verified against reviewed commit","",
      "- Archived source: PropertyGPT/certora_projects/gho-core at Git commit "+SOURCE_COMMIT,
      "- Historic Certora reviewed commit (aave/gho-core): "+REVIEW_COMMIT,
      "- All 22 archived Solidity Git blobs are identical to that reviewed commit.",
      "- Eight of nine CVL spec blobs match exactly. The exception ghoDiscountRateStrategy.spec is shortened;",
      "  its only surviving active rule limitOnDiscountRate is literally identical to the reviewed version.",
      "- Report publication: March 7, 2023; review work January 30 – February 28, 2023.",
      "- PDF direct official provenance: "+PDF_URL,
      "- PDF SHA256: "+sha256(pdf),
      "- Original report preserved at resources/15/Aave_Gho_Formal_Verification_Report.pdf.",
      "- PDF transcript at reports/15.md is non-authoritative for visual glyphs; original PDF is canonical.",
      "",
      "## Inventory and result boundaries","",
      "- Exactly 116 source declarations: VariableDebtToken 22, flashMinter 6, ghoAToken 7, ghoDiscountRateStrategy 1, ghoToken 28, ghoVariableDebtToken 25, set 27.",
      "- erc20.spec and summarizations.spec are helper imports with zero active properties.",
      "- All 116 instances are conservatively incomplete owing to unresolved source-era Solidity dependencies, historical mocks and original Prover config; each example records its specific context. CVL syntax migration is not the reason.",
      "- Exact-target report VERIFIED attributions: "+str(sum(x[4]=="VERIFIED" for x in review)),
      "- Explicit NOT_STATED: "+str(sum(x[4]=="NOT_STATED" for x in review))+
      " (including diagnostics, generic imported specs and rules without individual report evidence).",
      "- Violated active source instances: 0. The report's violated timelock property is not an active source declaration.",
      "- Detection Outcome NO_FINDING follows only individually verified properties without an attributed named finding.",
      "- New spec index relationship rows: 116, strictly additive. No new bugs.csv row; four report findings preserved separately, not guessed from matching themes.",
      "",
      "## Individual report/source mismatches",""]
    for n,note in REPORT_MISMATCHES.items():metadata.append("- "+n+": "+note+".")
    metadata+=["",
      "## Semantic/verification assumptions","",
      "- The report assumes Aave V3 Pool correctness; setter-initialized references exist when checked.",
      "- It bounds loop unrolling to two iterations and assumes token amounts WAD, normalized index RAY and rate BPS.",
      "- Both imported set.spec and VariableDebtToken.spec contain many executable rules absent from the PDF's per-contract table. Those remain NOT_STATED rather than receiving generic reported status.",
      "- Diagnostic cover_len rules and should_fail probes carry UNMAPPED instead of fabricated security labels.",
      "- The report lists a Low-severity rebalance timelock bypass under onlyRebalanceCanUpdateUserDiscountRate; after a removal commit it is no longer a true invariant, but that rule is not active in the source snapshot.",
      "- The report also documents Low maxFlashLoan/EIP3156 compliance, Low accumulated interest effects and an Informational WadRayMath convention. These report findings are distinct from Result/Detection Outcome in extracted CVL.",
      "- The published report mentions additional rules absent in PropertyGPT's reduced discount spec; do not add them to this snapshot.",
      "- Historical Solidity and CVL sources were preserved byte-for-byte, not replaced by current deployed contracts.",
      "",
      "## Coverage matrix",
      "",
      "| ID | Archived spec | Property | Target | Result | Bug Label |",
      "| ---: | --- | --- | --- | --- | --- |"]
    for i,src,n,target,result,label in review:
        metadata.append(f"| {i} | {src} | {n} | {target} | {result} | {label} |")
    metadata+=["",
      "## Required reproducible checks","",
      "- python scripts/check_specs.py . (in Web3Bugs-certora)",
      "- python scripts/check_contests_csv.py . (in Web3Bugs-certora)",
      "- python scripts/check_contracts.py . (in Web3Bugs-certora)",
      "- git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD (Git root)",
      "- Structural PASS does not mean Certora Prover was rerun. CI logs supply actual exit codes and checkout SHA.",
      "- Local ZIP inspection could not run because the supplied local Python/container infrastructure failed; a real GitHub Actions checkout is used instead.",
      ""]
    (DATA/"docs/spec_catalog_project_15.md").write_text("\n".join(metadata)+"\n")
    # External source byte identity and per-property fragment proof.
    for rel,_ in checked:
        assert (snapshot/rel).read_bytes()==(ARCHIVE/rel).read_bytes()
    for f in SPEC_FILES:assert (snapshot/f).read_bytes()==(ARCHIVE/f).read_bytes()
    for i,spec_name,name,target,result,label in review:
        seg=next(d["body"] for d in props[spec_name] if d["name"]==name)
        assert seg in (dest/f"{i}.spec").read_text(),(i,name)
        for ext in (".spec",".sol",".md",".txt"):
            assert (dest/f"{i}{ext}").is_file()
    assert len(list(dest.glob("*.spec")))==116
    assert len(list(dest.glob("*.sol")))==116
    assert len(list(dest.glob("*.md")))==116
    assert len(list(dest.glob("*.txt")))==116
    print("P15 SOURCE COMMIT",SOURCE_COMMIT,"REPORT COMMIT",REVIEW_COMMIT)
    print("P15 official PDF SHA256",sha256(pdf),"size",pdf.stat().st_size)
    print("P15 historical Solidity blobs identical",len(checked))
    print("P15 CVL spec blob differences",spec_drift)
    print("P15 116/116 literal property bodies, 116 incomplete quartets and 116 new CSV rows")
    print("P15 report VERIFIED",sum(x[4]=="VERIFIED" for x in review),"NOT_STATED",len(unverified))
    print("P15 NO VIOLATED SOURCE PROPERTIES (PDF violated property not active)")
    print("P15 labels",dict(collections.Counter(x[5] for x in review)))
if __name__=="__main__":run()
