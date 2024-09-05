import gspread
from config_reader import config

COLUMN_TITLES = ['Name', 'Username', 'Phone', 'English Level', 'Registration Time', 'Payment']
gc = gspread.service_account(filename=config.google_credentials_file)
sheet = gc.open(config.google_sheet_name).sheet1


def check_user_exists(username):
    existing_records = sheet.get_all_records()
    return any(record.get('Username') == f"@{username}" for record in existing_records)


def check_and_add_headers():
    headers = sheet.row_values(1)
    if headers != COLUMN_TITLES:
        sheet.insert_row(COLUMN_TITLES, 1)


def save_user_data_to_sheet(user_data):
    row = [
        user_data.get('name'),
        f"@{user_data.get('username')}",
        user_data.get('phone'),
        user_data.get('english_level'),
        user_data.get('registration_time'),
        user_data.get('Payment', 'NO')
    ]
    sheet.append_row(row)


def delete_old_record_and_add_new(user_data):
    username = user_data.get('username')
    existing_records = sheet.get_all_records()

    for index, record in enumerate(existing_records):
        if record.get('Username') == f"@{username}":
            sheet.delete_rows(index + 2)
            break

    save_user_data_to_sheet(user_data)


def update_payment_status(username):
    existing_records = sheet.get_all_records()
    for index, record in enumerate(existing_records):
        if record.get('Username') == f"@{username}":
            row_number = index + 2
            sheet.update_cell(row_number, COLUMN_TITLES.index('Payment') + 1, 'TRUE')
            break


def check_user_data(username):
    existing_records = sheet.get_all_records()
    for record in existing_records:
        if record.get('Username') == f"@{username}":
            return record
    return None
