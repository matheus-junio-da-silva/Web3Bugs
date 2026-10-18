// Project 10 example 179; handler HCEther, property cubeCounterIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
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

// Source: contracts/10/specs/harnesses/ProxyHarness.sol original lines 30-36 (literal excerpt)
        return _getSender();
    }

    function getCubeCounter() public view returns (uint256) {
        return _getCubeCounter();
    }
