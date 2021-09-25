
First we need to make a virtual environment to install all dependecies:
>virtualenv venv

Then we activate the virtual environment:
source venv/bin/activate    (if on linux or mac)
Scripts/bin/activate        (if on windows)

We install the required dependencies for this project:
>pip install -r /requirements.txt

Run the following command to get the Flask API started to get the endpoints to the Blockchain Network:
>python3 main.py
You are all set to view the blockchain and use it.
The endpoints and therir functionalities are listed below :
GET endpoints=>
                
                                
                



POST endpoints=>
                

                



                
Our blockchain have the following functionalities:
1.a) Get all the information of the Blockchain for the User.
  b) Immutability of the Blockchain (No one can change the already committed information without having to recompile the whole chain again)
  c) The timestamp of each Transaction is readily available using both the chain endpoint and time endpoint
  d) All the completed transactions are stored in the blockchain, we have both a verified (mined) pool as well as pending transactions.
2. We have also implemented a basic Proof of Work Algorithm where the hash of the block has to start with x numbers of 0's. We can set the difficulty (x) using the difficulty parameter in the BlockChain class
3. The value of each nonce is calculated using the Proof of Work algorithm
4. Each Block may contain multiple transactions, it can also contain a single transaction
5. The hash of the block and its previous block is available in the blockchain
6.Merkel tree yet to be made but.....(ho jayega ye bhi)
7.