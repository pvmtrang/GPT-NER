# coding: utf8
import os
import json

lines = [" Bác sĩ Trần Thanh Linh , từ Bệnh viện Chợ Rẫy chi viện phụ trách đơn nguyên hồi sức tích cực , cho biết \" bệnh nhân @@416## \" vẫn đang duy trì ECMO , thở máy , hiện xơ phổi rất nhiều .", " Bác sĩ Trần Thanh Linh , từ Bệnh viện Chợ Rẫy chi viện phụ trách đơn nguyên hồi sức tích cực , cho biết \" bệnh nhân 416 @@\"## vẫn đang duy trì ECMO , thở máy , hiện xơ phổi rất nhiều .", " Bác sĩ Trần Thanh Linh , từ Bệnh viện Chợ Rẫy chi viện phụ trách đơn nguyên hồi sức tích cực , cho biết \" bệnh nhân 416 \" vẫn đang duy trì ECMO , thở máy , hiện xơ phổi rất nhiều .", " Bác sĩ Trần Thanh Linh , từ Bệnh viện Chợ Rẫy chi viện phụ trách đơn nguyên hồi sức tích cực , cho biết \" bệnh nhân 416 \" vẫn đang duy trì ECMO , thở máy , hiện xơ phổi rất nhiều .", " Bác sĩ Trần Thanh Linh , từ Bệnh viện Chợ Rẫy chi viện phụ trách @@đơn nguyên hồi sức## tích cực , cho biết \" bệnh nhân 416 \" vẫn đang duy trì ECMO , thở máy , hiện xơ phổi rất nhiều .", " Bác sĩ Trần Thanh Linh , từ @@Bệnh viện Chợ Rẫy## chi viện phụ trách đơn nguyên hồi sức tích cực , cho biết \" bệnh nhân 416 \" vẫn đang duy trì ECMO , thở máy , hiện xơ phổi rất nhiều .", " Bác sĩ Trần Thanh Linh , từ @@Bệnh viện Chợ Rẫy## chi viện phụ trách đơn nguyên hồi sức tích cực , cho biết \" bệnh nhân 416 \" vẫn đang duy trì ECMO , thở máy , hiện xơ phổi rất nhiều .", " Bác sĩ Trần Thanh Linh , từ Bệnh viện Chợ Rẫy chi viện phụ trách đơn nguyên hồi sức tích cực , cho biết \" bệnh nhân 416 \" vẫn đang duy trì ECMO , thở @@máy## , hiện xơ phổi rất nhiều .", " Bác sĩ Trần Thanh Linh , từ Bệnh viện Chợ Rẫy chi viện phụ trách đơn nguyên hồi sức tích cực , cho biết \" bệnh nhân 416 \" vẫn đang duy trì ECMO , thở máy , hiện xơ phổi rất nhiều .", " Bác sĩ Trần Thanh Linh , từ Bệnh viện Chợ Rẫy chi viện phụ trách đơn nguyên hồi sức tích cực , cho biết \" bệnh nhân 416 \" vẫn đang duy trì ECMO , thở máy , hiện xơ phổi rất nhiều ."]

file_name = "logs\log_test.txt"
# with open(file_name, 'w', encoding='utf-8') as out_file:
    # json.dump(lines, out_file, ensure_ascii=False)


with open(file_name, "w",encoding='utf-8') as file:
    file.writelines( "%s\n" % item for item in lines )