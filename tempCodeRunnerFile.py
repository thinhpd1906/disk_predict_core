if __name__ == '__main__':
    username, password = get_user_credentials()
    token = authenticate(username, password)
    if token:
        device = Device()
        device.get_current_folder()
        device.get_device_name() 
        device.get_device_serial_number()
        convertInput = ConvertInput()
        model = Model(device.current_directory)
        insert_query = create_insert_smart_important()

        # device.get_smart_infor()  
        # b = model.test_predict(a_array)
        # print(b)
        # print(a)


        def test(): 
            device.get_smart_infor_linux()
            smart_infor, smart_important = convertInput.convert(device.smart)
            class_heath = model.predict(smart_infor)
            smart_important["class_prediction"] = class_heath[0].item()
            smart_important["serial_number"] = device.serial_number
            smart_important["date"] = get_time_now()
            print(class_heath, smart_important)
            try:
                create_smart(token, smart_important)
                # connection, cursor = fconnect_db()       
                # connection, cursor = fconnect_db_prod()       
                # cursor.execute(insert_query, smart_important)
                # connection.commit()
            except mysql.connector.Error as err:
                # print("Error: ", err)
                print("fail to insert smart infor")
            # finally:
                # close_connection(connection, cursor)
        test()
        schedule.every(4).seconds.do(test) 
        while True: 
            schedule.run_pending() 
            # time.sleep(1)
    else: 
        print("")


    # device = Device()
    # device.get_current_folder()
    # model = Model(device.current_directory)
    # for a in dt_1:
    #     a_array = np.array(a)
    #     print(a_array.size)
    #     a_array = a_array.reshape(1, 54, 1)
    #     b = model.test_predict(a_array)
    #     bno = b[0]
    #     value_15th = a_array[0, 15, 0]
    #     value_19th = a_array[0, 19, 0]
    #     value_35th = a_array[0, 35, 0]
    #     value_39th = a_array[0, 39, 0]
    #     value_1th = a_array[0, 1, 0]
    #     timestamp = "2024-06-01 08:00"
    #     serial_number= "Z302A13D"
    #     print(f"{value_15th}, {value_19th}, {value_35th}, {value_39th},  {value_1th}, {timestamp}, {bno}, {serial_number}") 
