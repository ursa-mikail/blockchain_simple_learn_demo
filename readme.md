# Blockchain Simple Learning Demo

The first transaction in a block is a transaction that starts a new coin owned by the creator of the block. This adds an incentive for nodes to support the network, and provides a way to initially distribute coins into circulation, since there is no central authority to issue them. The steady addition of a constant amount of new coins is analogous to gold miners expending resources to add gold to circulation. In our case, it is CPU time and electricity that is expended. The incentive can also be funded with transaction fees. If the output value of a transaction is less than its input value, the difference is a transaction fee that is added to the incentive value of the block containing the transaction. Once a predetermined number of coins have entered circulation, the incentive can transition entirely to transaction fees and be completely inflation free. The incentive may help encourage nodes to stay honest. If a greedy attacker is able to assemble more CPU power than all the honest nodes, he would have to choose between using it to defraud people by stealing back his payments, or using it to generate new coins. He ought to find it more profitable to play by the rules, such rules that favor him with more new coins than everyone else combined, than to undermine the system and the validity of his own wealth.

* Every time someone creates a transaction, they are the block creator. 

The miner will broadcast the answer. To get a reward, s/he appends a term before s/he starts mining. This also mints new currency amount.  
* Miners not demonstrated in this learning segment. 

<b>Note</b>
```
Visa: avg: 1700 tps, >24000 tps; bitcoin block size: 2400 transaction limit.
Mempool (transaction pool): list of outstanding transaction which have been broadcast but not in blockchain yet.
With more than 51%, attacker has higher chance to win the game, suppress mempool transaction selection and create double spending fraud and change rules of consensus.

BTC consensus: ledger append-only, decentralism, validation via miners and PoW  
```

![blockchain-describe](blockchain-describe.png)

<b>Advantage</b>
```
Finality: On-chain payments made offer near-instant finality. Merchants don’t have to worry about canceled customer payments due to insufficient funds or other reasons.

24/7 availability.
```

<b>Innovations yet-to-be</b>
```
Near-instant settlement.

Interoperability: available for payments outside of the service provider, offering interoperability with other processors, networks, and wallets.

Programmability and composability: Developers can freely experiment and build on top of the digital currency both inside and outside of the service provider ecosystem. Consumers, merchants, and institutions can enjoy a wide range of third-party developer experiences that leverage it for payments and financial use cases.

Low transaction costs

Non-exclusive

Easy on and off ramps

Counterfraud and user safety and protection
```
