import { expect } from "chai";
import { ethers } from "hardhat";

describe("PLT", function () {
  it("Verify your acceptance criteria of PLT transfer (1mln PLT)", async function () {
    const PLTToken = await ethers.getContractFactory("PLTToken");
    const initialSupply = 1000000;
    const first = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266";
    const second = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8";
    const pltObj = await PLTToken.deploy(initialSupply);
    await pltObj.deployed();
    expect(await pltObj.balanceOf(first)).to.equal(initialSupply);
    expect(await pltObj.balanceOf(second)).to.equal(0);
    await pltObj.transfer(second, initialSupply);
    expect(await pltObj.balanceOf(second)).to.equal(initialSupply);
    expect(await pltObj.balanceOf(first)).to.equal(0);
  });
});
