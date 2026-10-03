// Extracted from: contracts/2/contracts/ProofOfReserveAggregator.sol
// Original source range: 17-21

  /// @dev token address => proof or reserve feed
  mapping(address => address) internal _proofOfReserveList;

  /// @dev token address = > bridge wrapper
  mapping(address => address) internal _bridgeWrapperList;

// Extracted from: contracts/2/contracts/ProofOfReserveAggregator.sol
// Original source range: 24-39

  function getProofOfReserveFeedForAsset(address asset)
    external
    view
    returns (address)
  {
    return _proofOfReserveList[asset];
  }

  /// @inheritdoc IProofOfReserveAggregator
  function getBridgeWrapperForAsset(address asset)
    external
    view
    returns (address)
  {
    return _bridgeWrapperList[asset];
  }

// Extracted from: contracts/2/contracts/ProofOfReserveAggregator.sol
// Original source range: 42-85

  function enableProofOfReserveFeed(address asset, address proofOfReserveFeed)
    external
    onlyOwner
  {
    require(asset != address(0), 'INVALID_ASSET');
    require(proofOfReserveFeed != address(0), 'INVALID_PROOF_OF_RESERVE_FEED');
    require(_proofOfReserveList[asset] == address(0), 'FEED_ALREADY_ENABLED');

    _proofOfReserveList[asset] = proofOfReserveFeed;
    emit ProofOfReserveFeedStateChanged(
      asset,
      proofOfReserveFeed,
      address(0),
      true
    );
  }

  /// @inheritdoc IProofOfReserveAggregator
  function enableProofOfReserveFeedWithBridgeWrapper(
    address asset,
    address proofOfReserveFeed,
    address bridgeWrapper
  ) external onlyOwner {
    require(asset != address(0), 'INVALID_ASSET');
    require(proofOfReserveFeed != address(0), 'INVALID_PROOF_OF_RESERVE_FEED');
    require(bridgeWrapper != address(0), 'INVALID_BRIDGE_WRAPPER');
    require(_proofOfReserveList[asset] == address(0), 'FEED_ALREADY_ENABLED');

    _proofOfReserveList[asset] = proofOfReserveFeed;
    _bridgeWrapperList[asset] = bridgeWrapper;

    emit ProofOfReserveFeedStateChanged(
      asset,
      proofOfReserveFeed,
      bridgeWrapper,
      true
    );
  }

  /// @inheritdoc IProofOfReserveAggregator
  function disableProofOfReserveFeed(address asset) external onlyOwner {
    delete _proofOfReserveList[asset];
    delete _bridgeWrapperList[asset];
    emit ProofOfReserveFeedStateChanged(asset, address(0), address(0), false);

