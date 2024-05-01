import pytest


def test_smoke(acct1, acct2, acct3, contract_sbt):
    assert acct1.balance > 0
    assert acct2.balance > 0
    assert acct3.balance > 0
    assert contract_sbt.name() == "DDAcademy"
    assert contract_sbt.symbol() == "DDA"


def test_token_count_increments(acct1, acct2, contract_sbt):
    assert contract_sbt.totalSupply() == 0
    contract_sbt.safeMint(acct2, sender=acct1)
    contract_sbt.safeMint(acct2, sender=acct1)
    contract_sbt.safeMint(acct2, sender=acct1)
    assert contract_sbt.balanceOf(acct2) == 3
    assert contract_sbt.totalSupply() == 3


def test_set_base_uri(acct1, contract_sbt):
    assert contract_sbt.baseURI() == "https://academy.developerdao.com/credentials/"
    contract_sbt.setBaseURI("http://127.0.0.1:5000", sender=acct1)
    assert contract_sbt.baseURI() == "http://127.0.0.1:5000"


def test_get_token_uri(acct1, acct2, contract_sbt):
    contract_sbt.safeMint(acct2, sender=acct1)
    assert contract_sbt.tokenURI(0) == "https://academy.developerdao.com/credentials/0"


def test_contract_owner_can_mint_tokens(acct1, acct2, contract_sbt):
    assert contract_sbt.balanceOf(acct2) == 0
    contract_sbt.safeMint(acct2, sender=acct1)
    assert contract_sbt.balanceOf(acct2) == 1


def test_owner_cannot_transfer_own_token(acct1, acct2, contract_sbt):
    contract_sbt.safeMint(acct2, sender=acct1)
    with pytest.raises(Exception, match="Soulbound: Transfer failed"):
        contract_sbt.transferFrom(acct2, acct1, 0, sender=acct2)


def test_deployer_cannot_transfer_tokens(acct1, acct2, contract_sbt):
    contract_sbt.safeMint(acct2, sender=acct1)
    with pytest.raises(Exception, match="Soulbound: Transfer failed"):
        contract_sbt.transferFrom(acct2, acct1, 0, sender=acct1)


def test_deployer_cannot_safe_transfer_tokens(acct1, acct2, contract_sbt):
    contract_sbt.safeMint(acct2, sender=acct1)
    with pytest.raises(Exception, match="Soulbound: Transfer failed"):
        contract_sbt.safeTransferFrom(acct2, acct1, 0, sender=acct1)


def test_token_owner_can_burn_token(acct1, acct2, contract_sbt):
    contract_sbt.safeMint(acct2, sender=acct1)
    assert contract_sbt.balanceOf(acct2) == 1
    contract_sbt.burn(0, sender=acct2)
    assert contract_sbt.balanceOf(acct2) == 0


### Additional optional functionality for the SBT:


# def test_contract_owner_can_burn_any_token(acct1, acct2, contract_sbt):
#     contract_sbt.safeMint(acct2, sender=acct1)
#     assert contract_sbt.balanceOf(acct2) == 1
#     contract_sbt.burn(0, sender=acct1)
#     assert contract_sbt.balanceOf(acct2) == 0


# def test_updated_contract_owner_can_burn_any_token(acct1, acct2, acct3, contract_sbt):
#     contract_sbt.safeMint(acct2, sender=acct1)
#     contract_sbt.transferOwnership(acct3, sender=acct1)
#     assert contract_sbt.balanceOf(acct2) == 1
#     contract_sbt.burn(0, sender=acct3)
#     assert contract_sbt.balanceOf(acct2) == 0


# def test_outdated_contract_owner_cannot_burn_any_token(acct1, acct2, acct3, contract_sbt):
#     contract_sbt.safeMint(acct2, sender=acct1)
#     contract_sbt.transferOwnership(acct3, sender=acct1)
#     with pytest.raises(Exception, match="Soulbound: no burn except by owner"):
#         contract_sbt.burn(0, sender=acct1)
        

# def test_approve_function_is_prohibited(acct1, acct2, contract_sbt):
#     contract_sbt.safeMint(acct1, sender=acct1)
#     with pytest.raises(Exception, match="Soulbound: no approvals"):
#         contract_sbt.approve(acct2, 0, sender=acct1)
#
#
# def test_approve_all_function_is_prohibited(acct1, acct2, contract_sbt):
#     contract_sbt.safeMint(acct1, sender=acct1)
#     with pytest.raises(Exception, match="Soulbound: no approvals"):
#         contract_sbt.setApprovalForAll(acct2, True, sender=acct1)
