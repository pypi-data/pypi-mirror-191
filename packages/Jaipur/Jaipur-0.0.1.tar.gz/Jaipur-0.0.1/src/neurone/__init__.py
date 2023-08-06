def put_to_csv(NumpyArray,RelativeFilePath):
    data=NumpyArray
    str_Data = ""
    for pre in range(data.shape[1]):
        if data.shape[1] - 1 == pre:
            str_Data += "["+str(pre)+"]"+"\n"
            break
        str_Data += "["+str(pre)+"]"+","

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data.shape[1] - 1 == j:
                str_Data += str(data[i][j])
                break
            str_Data += str(data[i][j]) + ","

        if data.shape[0] - 1 == i and data.shape[1] - 1 == j:
            break
        str_Data += "\n"

    csv = open(RelativeFilePath, 'w')
    csv.write(str_Data)
    csv.close()

