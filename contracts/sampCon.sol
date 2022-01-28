// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// this is the sample first contract to check the functionality of the proxy
// this contract just store the value and return the value 
contract sampCon {

    uint256 public value;
    event changedValue(uint256 value);

    function retrive() public view returns (uint256) {
        return value;
    } 

    function store(uint256 _value ) public {
        value = _value;
        emit changedValue(value);
    }

  
}
