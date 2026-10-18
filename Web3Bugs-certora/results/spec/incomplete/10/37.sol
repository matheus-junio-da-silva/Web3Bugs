// Historical target HMaker; exact Solidity excerpt
// Source: contracts/10/contracts/handlers/maker/HMaker.sol lines 1-70
// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "./IDSProxy.sol";
import "./IMaker.sol";
import "../HandlerBase.sol";

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract HMaker is HandlerBase {
    using SafeERC20 for IERC20;
    using LibStack for bytes32[];

    // prettier-ignore
    address public constant PROXY_REGISTRY = 0x4678f0a6958e4D2Bc4F1BAF7Bc52E8F3564f3fE4;
    // prettier-ignore
    address public constant DAI_TOKEN = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    // prettier-ignore
    address public constant CHAIN_LOG = 0xdA0Ab1e0017DEbCd72Be8599041a2aa3bA7e740F;

    modifier cdpAllowed(uint256 cdp) {
        IMakerManager manager = IMakerManager(getCdpManager());
        address owner = manager.owns(cdp);
        address sender = _getSender();
        _requireMsg(
            IDSProxyRegistry(PROXY_REGISTRY).proxies(sender) == owner ||
                manager.cdpCan(owner, cdp, sender) == 1,
            "General",
            "Unauthorized sender of cdp"
        );
        _;
    }

    function getContractName()
        public
        pure
        virtual
        override
        returns (string memory)
    {
        return "HMaker";
    }

    function getProxyActions() public pure virtual returns (address) {
        return 0x82ecD135Dce65Fbc6DbdD0e4237E0AF93FFD5038;
    }

    function getCdpManager() public pure virtual returns (address) {
        return 0x5ef30b9986345249bc32d8928B7ee64DE9435E39;
    }

    function getMcdJug() public view returns (address) {
        return IMakerChainLog(CHAIN_LOG).getAddress("MCD_JUG");
    }

    function openLockETHAndDraw(
        uint256 value,
        address ethJoin,
        address daiJoin,
        bytes32 ilk,
        uint256 wadD
    ) external payable returns (uint256 cdp) {
        IDSProxy proxy = IDSProxy(_getProxy(address(this)));
        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);

        try
            proxy.execute{value: value}(
                getProxyActions(),

// Exact original Solidity: contracts/10/contracts/handlers/maker/HMaker.sol lines 170-201
    function safeLockGem(
        address gemJoin,
        uint256 cdp,
        uint256 wad
    ) external payable {
        IDSProxy proxy = IDSProxy(_getProxy(address(this)));
        address owner = _getProxy(_getSender());
        address token = IMakerGemJoin(gemJoin).gem();
        // if amount == type(uint256).max return balance of Proxy
        wad = _getBalance(token, wad);
        _tokenApprove(token, address(proxy), wad);
        try
            proxy.execute(
                getProxyActions(),
                abi.encodeWithSelector(
                    // selector of "safeLockGem(address,address,uint256,uint256,bool,address)"
                    0xead64729,
                    getCdpManager(),
                    gemJoin,
                    cdp,
                    wad,
                    true,
                    owner
                )
            )
        {} catch Error(string memory reason) {
            _revertMsg("safeLockGem", reason);
        } catch {
            _revertMsg("safeLockGem");
        }
        _tokenApproveZero(token, address(proxy));
    }


// Exact original Solidity: contracts/10/contracts/handlers/maker/HMaker.sol lines 203-227
    function freeETH(
        address ethJoin,
        uint256 cdp,
        uint256 wad
    ) external payable cdpAllowed(cdp) {
        // Check msg.sender authority
        IDSProxy proxy = IDSProxy(_getProxy(address(this)));
        try
            proxy.execute(
                getProxyActions(),
                abi.encodeWithSelector(
                    // selector of "freeETH(address,address,uint256,uint256)"
                    0x7b5a3b43,
                    getCdpManager(),
                    ethJoin,
                    cdp,
                    wad
                )
            )
        {} catch Error(string memory reason) {
            _revertMsg("freeETH", reason);
        } catch {
            _revertMsg("freeETH");
        }
    }
