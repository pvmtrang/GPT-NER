FULL_DATA = {
    "phoNER_COVID19" : {
        "PATIENT_ID": ("PATIENT_ID", "Unique identifier of a COVID-19 patient in Vietnam. An PATIENT_ID annotation over “X” refers to as the Xth patient having COVID-19 in Vietnam"),
        "NAME": ("NAME", "Name of a patient or person who comes into contact with a patient"),
        "AGE": ("AGE", "Age of a patient or person who comes into contact with a patient"),
        "GENDER": ("GENDER", "Gender of a patient or person who comes into contact with a patient"),
        "JOB": ("JOB", "Job of a patient or person who comes into contact with a patient"),
        "LOCATION": ("LOCATION", "Locations/places that a patient was presented at"),
        "ORGANIZATION": ("ORGANIZATION", "Organizations related to a patient, e.g. company, government organization, and the like, with structures and their own functions"),
        "SYMPTOM_AND_DISEASE": ("SYMPTOM_AND_DISEASE", "Symptoms that a patient experiences, and diseases that a patient had prior to COVID-19 or complications that usually appear in death reports"),
        "TRANSPORTATION": ("TRANSPORTATION", "Means of transportation that a patient used. Here, we only tag the specific identifier of vehicles, e.g. flight numbers and bus/car plates"),
        "DATE": ("DATE", "Any date that appears in the sentence")
    },
     "phoNER_COVID19_vie" : {
        "PATIENT_ID": ("PATIENT_ID", "là số định danh cho một bệnh nhân mắc COVID-19 tại Việt Nam. Một bệnh nhân có số PATIENT_ID X nghĩa là bệnh nhân đó là người thứ X mắc COVID-19 tại Việt Nam"),
        "NAME": ("NAME", "là tên của bệnh nhân mắc COVID-19 hoặc của người có tiếp xúc với bệnh nhân COVID-19"),
        "AGE": ("AGE", "là tuổi của bệnh nhân COVID-19 hoặc của người có tiếp xúc với bệnh nhân"),
        "GENDER": ("GENDER", "là giới tính của bệnh nhân COVID-19 hoặc người có tiếp xúc với bệnh nhân"),
        "JOB": ("JOB", "là công việc, nghề nghiệp của bệnh nhân COVID-19 hoặc người có tiếp xúc với bệnh nhân"),
        "LOCATION": ("LOCATION", "là các địa điểm, những nơi mà bệnh nhân COVID-19 đã đến"),
        "ORGANIZATION": ("ORGANIZATION", "là các tổ chức có liên quan đến bệnh nhân COVID-19 ví dụ như công ty, doanh nghiệp, tổ chức chính phủ, cơ quan"),
        "SYMPTOM_AND_DISEASE": ("SYMPTOM_AND_DISEASE", "là các triệu chứng mà bệnh nhân COVID-19 mắc phải, hoặc các bệnh mà bệnh nhân đã có trước khi mắc COVID-19, hoặc các biến chứng khác thường thấy trong báo cáo tử vong, trong hồ sơ bệnh án"),
        "TRANSPORTATION": ("TRANSPORTATION", "là biến số xe máy, biển số xe ô tô, số hiệu máy bay, xe bus, hay của các phương tiện giao thông mà bệnh nhân COVID-19 sử dụng"),
        "DATE": ("DATE", "là tất cả ngày, ngày tháng xuất hiện trong câu")
    },
    "CONLL": {
        "ORG": ("organization", "are limited to named corporate, governmental, or other organizational entities"),
        "PER": ("person", "are named persons or family"),
        "LOC": ("location", "are the name of politically or geographically defined locations such as cities, provinces, countries, international regions, bodies of water, mountains, etc"),
        "MISC": ("miscellaneous", "include events, nationalities, products and works of art")
    },
    "Ontonotes5.0": {
        "PERSON": ("person", "are people, including fictional"),
        "NORP": ("nationality", "are nationalities or religious or political groups but do not include countries, cities, or states"),
        "FAC": ("facility", "are buildings, airports, highways, bridges, etc"),
        "ORG": ("organization", "are companies, agencies, institutions, etc"),
        "GPE": ("country", "are countries, cities, states"),
        "LOC": ("location", "are non-GPE locations, mountain ranges, bodies of water"),
        "PRODUCT": ("product", "are vehicles, weapons, foods, etc"),
        "EVENT": ("event", "are named hurricanes, battles, wars, sports events, etc"),
        "WORK_OF_ART": ("work of art", "are titles of books, songs, etc"),
        "LAW": ("law", "are named documents made into laws"),
        "LANGUAGE": ("language", "are any named language"),
        "DATE": ("date", "are absolute or relative dates or periods"),
        "TIME": ("time", "are times smaller than a day"),
        "PERCENT": ("percent", "means percentage (including \"%\")"),
        "MONEY": ("money", "are monetary values, including unit"),
        "QUANTITY": ("quantity", "are measurements, as of weight or distance"),
        "ORDINAL": ("ordinal", "are \"first\", \"second\", etc"),
        "CARDINAL": ("cardinal", "are numerals that do not fall under another type")
    },
    "ACE2004": {
        "GPE": ("geographical political", "are geographical regions defined by political and or social groups such as countries, nations, regions, cities, states, government and its people"),
        "ORG": ("organization", "are limited to companies, corporations, agencies, institutions and other groups of people"),
        "PER": ("person", "are limited to human including a single individual or a group"),
        "FAC": ("facility", "are limited to buildings and other permanent man-made structures such as buildings, airports, highways, bridges"),
        "VEH": ("vehicle", "are physical devices primarily designed to move, carry, pull or push the transported object such as helicopters, trains, ship and motorcycles"),
        "LOC": ("location", "are limited to geographical entities such as geographical areas and landmasses, mountains, bodies of water, and geological formations"),
        "WEA": ("weapon", "are limited to physical devices such as instruments for physically harming such as guns, arms and gunpowder")
    },
    "ACE2005": {
        "GPE": ("geographical political", "are geographical regions defined by political and or social groups such as countries, nations, regions, cities, states, government and its people"),
        "ORG": ("organization", "are limited to companies, corporations, agencies, institutions and other groups of people"),
        "PER": ("person", "are limited to human including a single individual or a group"),
        "FAC": ("facility", "are limited to buildings and other permanent man-made structures such as buildings, airports, highways, bridges"),
        "VEH": ("vehicle", "are physical devices primarily designed to move, carry, pull or push the transported object such as helicopters, trains, ship and motorcycles"),
        "LOC": ("location", "are limited to geographical entities such as geographical areas and landmasses, mountains, bodies of water, and geological formations"),
        "WEA": ("weapon", "are limited to physical devices such as instruments for physically harming such as guns, arms and gunpowder")
    },
    "GENIA": {
        "cell_line": ("cell line", "indicate cell line"),
        "cell_type": ("cell type", "indicate cell type"),
        "DNA": ("DNA", "indicate DNA"),
        "RNA": ("RNA", "indicate RNA"),
        "protein": ("protein", "indicate protein"),
    },
    "MSRA": {
        "NS": ("NS", "按照地理位置划分的国家，城市，乡镇，大洲"),
        "NR": ("NR", "人名和虚构的人物形象"),
        "NT": ("NT", "组织包括公司，政府党派，学校，政府，新闻机构"),
    },
    "ZHONTO": {
        "LOC": ("LOC", "山脉,河流自然景观的地点"),
        "PER": ("PER", "人名和虚构的人物形象"),
        "GPE": ("GPE", "按照国家,城市,州县划分的地理区域"),
        "ORG": ("ORG", "组织包括公司,政府党派,学校,政府,新闻机构"),
    }
}
