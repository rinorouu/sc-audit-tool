// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Vulnerable {
    mapping(address => uint) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() external {
        uint balance = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer failed");
        balances[msg.sender] = 0;
    }
}
