import os
import json
from web3 import Web3

# build 디렉토리의 파일 목록 나열
build_directory = "build"
files = os.listdir(build_directory)
print(f"Files in build directory: {files}")

# 필요한 파일들 지정
bytecode_file = "contracts_ContactStorage_sol_ContactStorage.bin"
abi_file = "contracts_ContactStorage_sol_ContactStorage.abi"

# 컴파일된 컨트랙트 정보 읽기
with open(os.path.join(build_directory, bytecode_file), "r") as f:
    bytecode = "0x" + f.read().strip()

with open(os.path.join(build_directory, abi_file), "r") as f:
    abi = json.load(f)

# Ganache에 연결
w3 = Web3(Web3.HTTPProvider("http://ganache:8545"))

# Ganache의 첫 번째 계정 사용
my_address = w3.eth.accounts[0]
private_key = "0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3"  # Ganache의 첫 번째 계정의 개인 키

# 컨트랙트 배포
Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
chain_id = 1337
nonce = w3.eth.get_transaction_count(my_address)

# 트랜잭션 생성
transaction = {
    'nonce': nonce,
    'gasPrice': w3.eth.gas_price,
    'gas': 2000000,
    'to': '',
    'value': 0,
    'data': Contract.constructor().data_in_transaction,
    'chainId': chain_id,
    'from': my_address
}

# 트랜잭션 서명 및 전송
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# 배포된 컨트랙트 주소 출력
contract_address = tx_receipt.contractAddress
print(f"Contract deployed at {contract_address}")

# 컨트랙트 주소와 ABI를 JSON 파일로 저장
contract_data = {
    "address": contract_address,
    "abi": abi
}
with open("contract_data.json", "w") as outfile:
    json.dump(contract_data, outfile)
print("Contract address and ABI have been saved to contract_data.json")

# 컴파일된 컨트랙트 ABI 및 주소 불러오기
contract = w3.eth.contract(address=contract_address, abi=abi)


# 트랜잭션 실행 및 디버깅을 위한 함수 정의
def add_contact_and_debug(contract, name, email, phone):
    try:
        # 가스 추정
        estimated_gas = contract.functions.addContact(name, email, phone).estimateGas({'from': my_address})
        print(f"Estimated Gas: {estimated_gas}")

        # 트랜잭션 실행
        tx_hash = contract.functions.addContact(name, email, phone).transact({
            'from': my_address,
            'gas': estimated_gas + 100000  # 안전 마진 추가
        })

        # 트랜잭션 영수증 가져오기
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction Receipt: {tx_receipt}")
        if tx_receipt['status'] == 1:
            print("Transaction succeeded")
        else:
            print("Transaction failed")
            # 트랜잭션 디버깅 정보 출력
            print(f"Transaction logs: {tx_receipt['logs']}")

    except Exception as e:
        print(f"Error adding contact: {str(e)}")


# 트랜잭션 실행
name = "Alice"
email = "alice@example.com"
phone = "123-456-7890"
add_contact_and_debug(contract, name, email, phone)


# 연락처 확인 함수
def check_contact_count_and_retrieve():
    try:
        # contactCount 확인
        contact_count = contract.functions.contactCount().call({'from': my_address})
        print(f"Contact count: {contact_count}")

        # 각 연락처 정보 출력
        for i in range(1, contact_count + 1):
            try:
                contact = contract.functions.getContact(i).call({'from': my_address})
                print(f"Contact {i}: Name={contact[0]}, Email={contact[1]}, Phone={contact[2]}")
            except Exception as e:
                print(f"Error getting contact {i}: {str(e)}")

    except Exception as e:
        print(f"Error retrieving contact count: {str(e)}")


check_contact_count_and_retrieve()
