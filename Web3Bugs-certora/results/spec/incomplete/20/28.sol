// Historical source: contracts/20/spec/harness/RebaseWrapper.sol:1-76
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import "@boringcrypto/boring-solidity/contracts/libraries/BoringRebase.sol";

contract RebaseWrapper {
    using BoringMath for uint256;
    using BoringMath128 for uint128;
	using RebaseLibrary for Rebase;

	Rebase public rebase;

    function getElastic() public view returns (uint128) {
        return rebase.elastic;
    }

    function getBase() public view returns (uint128) {
        return rebase.base;
    }

    function toBase(uint256 elastic, bool roundUp) public view returns (uint256 base) {
        base = rebase.toBase(elastic, roundUp);
    }

    /** Equivalent to toBase when roundUp parameter is "false", but a bit 
        easier on the smt solver. */
    function toBaseFloor(uint256 elastic) public view returns (uint256 base) {
        if (rebase.elastic == 0) {
            base = elastic;
        } else {
            base = elastic.mul(rebase.base) / rebase.elastic;
        }
    }

    function toElastic(uint256 base, bool roundUp) public view returns (uint256 elastic) {
        return rebase.toElastic(base, roundUp);
    }


    function add(uint256 addAmount, bool roundUp) public returns (uint256 base) {
        uint256 addAmountBase;
        (rebase, addAmountBase) = rebase.add(addAmount, roundUp);
        return addAmountBase;
    }
    /** Equivalent to add when roundUp parameter is "false", but a bit 
        easier on the smt solver. */
    function addFloor(uint256 elastic) public  returns (uint256 base) {
        base = toBaseFloor(elastic);
        rebase.elastic = rebase.elastic.add(elastic.to128());
        rebase.base = rebase.base.add(base.to128());
        return base;
    }

    function add(uint256 addAmount, uint256 addShares) public {
        rebase = rebase.add(addAmount, addShares);
    }

    function sub(uint256 subAmount, bool roundUp) public returns (uint256 elastic) {
        uint256 subAmountElastic;
        (rebase, subAmountElastic) = rebase.sub(subAmount, roundUp);
        return subAmountElastic;
    }

    function sub(uint256 subAmount, uint256 subShares) public {
        rebase = rebase.sub(subAmount, subShares);
    }

    function addElastic(uint256 elastic) public returns(uint256 newElastic) {
       return rebase.addElastic(elastic);
    }

    function subElastic(uint256 elastic) public returns(uint256 newElastic) {
       return rebase.subElastic(elastic);
    }

}

// Historical source: contracts/20/contracts/flat/BentoBoxFlat.sol:236-279
struct Rebase {
    uint128 elastic;
    uint128 base;
}

/// @notice A rebasing library using overflow-/underflow-safe math.
library RebaseLibrary {
    using BoringMath for uint256;
    using BoringMath128 for uint128;

    /// @notice Calculates the base value in relationship to `elastic` and `total`.
    function toBase(
        Rebase memory total,
        uint256 elastic,
        bool roundUp
    ) internal pure returns (uint256 base) {
        if (total.elastic == 0) {
            base = elastic;
        } else {
            base = elastic.mul(total.base) / total.elastic;
            if (roundUp && base.mul(total.elastic) / total.base < elastic) {
                base = base.add(1);
            }
        }
    }

    /// @notice Calculates the elastic value in relationship to `base` and `total`.
    function toElastic(
        Rebase memory total,
        uint256 base,
        bool roundUp
    ) internal pure returns (uint256 elastic) {
        if (total.base == 0) {
            elastic = base;
        } else {
            elastic = base.mul(total.elastic) / total.base;
            if (roundUp && elastic.mul(total.base) / total.elastic < base) {
                elastic = elastic.add(1);
            }
        }
    }

    /// @notice Add `elastic` to `total` and doubles `total.base`.
    /// @return (Rebase) The new total.


// Historical source: contracts/20/contracts/flat/BentoBoxFlat.sol:281-340
    function add(
        Rebase memory total,
        uint256 elastic,
        bool roundUp
    ) internal pure returns (Rebase memory, uint256 base) {
        base = toBase(total, elastic, roundUp);
        total.elastic = total.elastic.add(elastic.to128());
        total.base = total.base.add(base.to128());
        return (total, base);
    }

    /// @notice Sub `base` from `total` and update `total.elastic`.
    /// @return (Rebase) The new total.
    /// @return elastic in relationship to `base`.
    function sub(
        Rebase memory total,
        uint256 base,
        bool roundUp
    ) internal pure returns (Rebase memory, uint256 elastic) {
        elastic = toElastic(total, base, roundUp);
        total.elastic = total.elastic.sub(elastic.to128());
        total.base = total.base.sub(base.to128());
        return (total, elastic);
    }

    /// @notice Add `elastic` and `base` to `total`.
    function add(
        Rebase memory total,
        uint256 elastic,
        uint256 base
    ) internal pure returns (Rebase memory) {
        total.elastic = total.elastic.add(elastic.to128());
        total.base = total.base.add(base.to128());
        return total;
    }

    /// @notice Subtract `elastic` and `base` to `total`.
    function sub(
        Rebase memory total,
        uint256 elastic,
        uint256 base
    ) internal pure returns (Rebase memory) {
        total.elastic = total.elastic.sub(elastic.to128());
        total.base = total.base.sub(base.to128());
        return total;
    }

    /// @notice Add `elastic` to `total` and update storage.
    /// @return newElastic Returns updated `elastic`.
    function addElastic(Rebase storage total, uint256 elastic) internal returns (uint256 newElastic) {
        newElastic = total.elastic = total.elastic.add(elastic.to128());
    }

    /// @notice Subtract `elastic` from `total` and update storage.
    /// @return newElastic Returns updated `elastic`.
    function subElastic(Rebase storage total, uint256 elastic) internal returns (uint256 newElastic) {
        newElastic = total.elastic = total.elastic.sub(elastic.to128());
    }
}

