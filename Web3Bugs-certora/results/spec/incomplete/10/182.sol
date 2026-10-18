// Project 10 example 182; handler HCEther, property noOverwrite. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/compound/HCEther.sol original lines 16-41
    }

    function mint(uint256 value) external payable returns (uint256) {
        ICEther compound = ICEther(CETHER);

        // Get cether balance of proxy before mint
        uint256 beforeCEtherAmount = compound.balanceOf(address(this));

        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);

        // Execute mint
        try compound.mint{value: value}() {} catch Error(string memory reason) {
            _revertMsg("mint", reason);
        } catch {
            _revertMsg("mint");
        }

        // Get cether balance of proxy after mint
        uint256 afterCEtherAmount = compound.balanceOf(address(this));

        // Update involved token
        _updateToken(CETHER);
        return (afterCEtherAmount - beforeCEtherAmount);
    }


// Source: contracts/10/contracts/handlers/compound/HCEther.sol original lines 40-65
    }

    function redeem(uint256 redeemTokens) external payable returns (uint256) {
        // Get ether balance of proxy before redeem
        uint256 beforeRedeemAmount = address(this).balance;

        // Approve cether
        ICEther compound = ICEther(CETHER);

        // if amount == type(uint256).max return balance of Proxy
        redeemTokens = _getBalance(CETHER, redeemTokens);

        // Execute redeem
        try compound.redeem(redeemTokens) returns (uint256 errorCode) {
            _requireMsg(
                errorCode == 0,
                "redeem",
                string(abi.encodePacked("error ", _uint2String(errorCode)))
            );
        } catch Error(string memory reason) {
            _revertMsg("redeem", reason);
        } catch {
            _revertMsg("redeem");
        }

        // Get ether balance of proxy after redeem

// Source: contracts/10/specs/harnesses/ProxyHarness.sol original lines 7-25 (literal excerpt)

    function getSlot(uint256 s) external view returns (uint256 x) {
        assembly {
            x := sload(s)
        }
    }

    function getStackLengthSlot() external view returns (uint256 x) {
        assembly {
            x := stack_slot
        }
    }

    function getStackLength() external view returns (uint256) {
        return stack.length;
    }

    function ethBalance(address who) external view returns (uint256) {
        return who.balance;
