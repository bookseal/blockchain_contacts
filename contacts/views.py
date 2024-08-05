import traceback
from web3 import Web3
from eth_utils import to_checksum_address
from django.conf import settings
from django.shortcuts import render, redirect
import json
import logging

logger = logging.getLogger(__name__)

# Web3 설정
w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_NODE_URL))

# 컨트랙트 설정
with open('contract_data.json', 'r') as f:
    contract_data = json.load(f)

contract_address = to_checksum_address(contract_data['address'])
contract_abi = contract_data['abi']
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Ganache 계정 설정
GANACHE_ACCOUNT = to_checksum_address("0x627306090abaB3A6e1400e9345bC60c78a8BEf57")

print(f"Contract Address from JSON: {contract_address}")
print(f"Contract ABI from JSON: {contract_abi}")
print(f"Ganache Account: {GANACHE_ACCOUNT}")
print(f"Is Web3 connected: {w3.isConnected()}")

def contact_list(request):
    logger.info("Entering contact_list view")
    logger.info(f"Contract Address: {contract_address}")
    logger.info(f"Is connected: {w3.isConnected()}")
    logger.info(f"Latest block: {w3.eth.block_number}")
    logger.info(f"Using account: {GANACHE_ACCOUNT}")
    logger.info(f"Ethereum Node URL: {settings.ETHEREUM_NODE_URL}")

    print(f"Contract Address in view: {contract_address}")
    print(f"Is connected in view: {w3.isConnected()}")
    print(f"Latest block in view: {w3.eth.block_number}")
    print(f"Using account in view: {GANACHE_ACCOUNT}")

    try:
        # 컨트랙트 코드 확인
        code = w3.eth.get_code(contract_address)
        logger.info(f"Contract code: {code.hex()}")
        print(f"Contract code: {code.hex()}")
        if code == b'':  # 계약 코드가 없다면
            raise ValueError("No contract deployed at the given address")

        # 블록체인에서 연락처 목록 가져오기
        contact_count = contract.functions.contactCount().call({'from': GANACHE_ACCOUNT})
        logger.info(f"Contact count: {contact_count}")
        print(f"Contact count: {contact_count}")
        contacts = []
        for i in range(1, contact_count + 1):
            try:
                name, email, phone = contract.functions.getContact(i).call({'from': GANACHE_ACCOUNT})
                contacts.append({'name': name, 'email': email, 'phone': phone})
                logger.info(f"Contact {i}: {name}, {email}, {phone}")
                print(f"Contact {i}: {name}, {email}, {phone}")
            except Exception as e:
                logger.error(f"Error getting contact {i}: {str(e)}")
                logger.error(traceback.format_exc())
                print(f"Error getting contact {i}: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting contact count: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"Error getting contact count: {str(e)}")
        contacts = []

    logger.info(f"Total contacts retrieved: {len(contacts)}")
    print(f"Total contacts retrieved: {len(contacts)}")
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})
def add_contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']

        print(f"Add Contact - Name: {name}, Email: {email}, Phone: {phone}")

        try:
            initial_count = contract.functions.contactCount().call({'from': GANACHE_ACCOUNT})
            print(f"Initial contact count: {initial_count}")

            tx_hash = contract.functions.addContact(name, email, phone).transact({
                'from': GANACHE_ACCOUNT,
                'gas': 6000000  # 가스 한도를 6,000,000으로 증가
            })

            # 트랜잭션 영수증 가져오기
            tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

            print(f"Transaction Receipt: {tx_receipt}")
            if tx_receipt['status'] == 1:
                print("Transaction succeeded")
            else:
                print("Transaction failed")
                # 트랜잭션 디버깅 정보 출력
                print(f"Transaction logs: {tx_receipt['logs']}")

            final_count = contract.functions.contactCount().call({'from': GANACHE_ACCOUNT})
            print(f"Final contact count: {final_count}")

            # 트랜잭션 이벤트 로그 가져오기
            logs = tx_receipt.logs
            for log in logs:
                print(f"Log: {log}")

        except Exception as e:
            print(f"Error adding contact: {str(e)}")
            print(traceback.format_exc())

        return redirect('contact_list')

    return render(request, 'contacts/add_contact.html')
