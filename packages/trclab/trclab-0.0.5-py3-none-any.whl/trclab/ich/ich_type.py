from enum import IntFlag, unique


@unique
class ICHType(IntFlag):
    # 沒有出血 （Not Any）
    NOT_ANY = 0
    # 腦實質出血 (Intraparenchymal Hemorrhage)
    INTRAPARENCHYMAL = 1
    # 腦室內出血 (Intraventricular Hemorrhage)
    INTRAVENTRICULAR = 2
    # 蜘蛛網膜下腔出血 (Subarachnoid Hemorrhage)
    SUBARACHNOID = 4
    # 硬腦膜下腔出血 (Subdural Hemorrhage)
    SUBDURAL = 8
    # 硬腦膜上出血 (Epidural Hemorrhage)
    EPIDURAL = 16
