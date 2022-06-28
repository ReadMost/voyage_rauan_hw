# My first knowledge in Blockchain:

A *token* contract is simply an Ethereum smart contract. "Sending tokens" actually means "calling a method on a smart contract that someone wrote and deployed". At the end of the day, a token contract is not much more than a mapping of addresses to balances, plus some methods to add and subtract from those balances.

info about tx: https://ethereum.org/en/developers/docs/transactions/#:~:text=An%20Ethereum%20transaction%20refers%20to,takes%20place%20within%20a%20transaction.

TYPES OF TRANSACTIONS
On Ethereum there are a few different types of transactions:

- Regular transactions: a transaction from one wallet to another.
- Contract deployment transactions: a transaction without a 'to' address, where the data field is used for the contract code.
- Execution of a contract: a transaction that interacts with a deployed smart contract. In this case, 'to' address is the smart contract address.
