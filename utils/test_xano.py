# from xano import XanoClient

# xano_client = XanoClient()

# # TEST 1:
# print("     Svi podaci iz tabele 'shops'     ")
# shops_data = xano_client.getAllTableData("shops")
# for shop in shops_data:
#     print('\n')
#     print(shop)
# print('\n_________________________________________________________________________________\n')
# # TEST 2:
# print("\n    Vrednosti iz kolone 'shop_name'     ")
# shop_names = xano_client.getColumnFromTable("shops", "shop_name")
# for name in shop_names:
#     print('\n')
#     print(name)
# print('\n_________________________________________________________________________________\n')
# # TEST 3: 
# print("\n     Svi podaci iz tabele 'provider  ")
# provider_data = xano_client.getAllTableData("provider")
# for provider in provider_data:
#     print('\n')
#     print(provider)
# print('\n_________________________________________________________________________________\n')
# # TEST 4:
# print("\n     Vrednosti iz kolone 'provider_name'     ")
# provider_names = xano_client.getColumnFromTable("provider", "provider_name")
# for name in provider_names:
#     print('\n')
#     print(name)

# #test 5

# print("\n     Svi podaci iz tabele 'trxactiverequest  ")
# trxactiverequest_data = xano_client.getAllTableData("trxactiverequest")
# for trxactiverequest in trxactiverequest_data:
#     print('\n')
#     print(trxactiverequest)
# print('\n_________________________________________________________________________________\n')
# # TEST 6
# print("\n     Vrednosti iz kolone 'provider_name'     ")
# merchant_names = xano_client.getColumnFromTable("trxactiverequest", "merchant_id")
# for name in merchant_names:
#     print('\n')
#     print(name)

from xano import XanoClient

# Kreiranje XanoClient instance
xano_client = XanoClient()

# ID transakcije koji proveravamo
transaction_id_to_check = "trx9876543210" 

# Novi red koji želimo dodati ako transaction_id ne postoji
new_transaction = {
    "transaction_Id": transaction_id_to_check,
    "merchant_id": 1,
    "provider_id": 2,
    "pg_id": "pg_example",
    "trx_id": "trx_example_001",
    "task_id_click_up": "task001",
    "provider_support_chat_message_id_tg": "chat123",
    "merchant_support_chat_message_id_tg": "chat456",
    "Closed": False,
    "Manual": False
}

# Provera i dodavanje reda
result = xano_client.transaction_id_exists(transaction_id_to_check, new_transaction)

if result:
    print("Succes add it")
else:
    print("Error acured")
