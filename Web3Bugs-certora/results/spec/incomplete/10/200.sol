// Project 10 example 200; handler HCurve, property noOverwrite. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/curve/HCurve.sol original lines 15-40

    /// @notice Curve exchange
    function exchange(
        address handler,
        address tokenI,
        address tokenJ,
        int128 i,
        int128 j,
        uint256 amount,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _amount,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _exchangeBefore(handler, tokenI, tokenJ, amount);
        try
            ICurveHandler(handler).exchange{value: ethAmount}(
                i,
                j,
                _amount,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("exchange", reason);
        } catch {

// Source: contracts/10/contracts/handlers/curve/HCurve.sol original lines 46-71

    /// @notice Curve exchange with uint256 ij
    function exchangeUint256(
        address handler,
        address tokenI,
        address tokenJ,
        uint256 i,
        uint256 j,
        uint256 amount,
        uint256 minAmount
    ) external payable returns (uint256) {
        (
            uint256 _amount,
            uint256 balanceBefore,
            uint256 ethAmount
        ) = _exchangeBefore(handler, tokenI, tokenJ, amount);
        try
            ICurveHandler(handler).exchange{value: ethAmount}(
                i,
                j,
                _amount,
                minAmount
            )
        {} catch Error(string memory reason) {
            _revertMsg("exchangeUint256", reason);
        } catch {

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
