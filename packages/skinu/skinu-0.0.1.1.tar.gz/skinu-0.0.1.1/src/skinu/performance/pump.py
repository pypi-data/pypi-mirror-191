import math


class PerformancePump:
    ALL_ITEMS = ["head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor",
                 "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"]

    def __init__(self):
        pass

    # =========================================
    # method 선택
    # =========================================
    def _select_method_num(self, p_in_doc: dict) -> int:
        tmp_method_num = 0

        tmp_chk_hea = p_in_doc["head"]["check"]
        tmp_chk_suc = p_in_doc["suction_pressure"]["check"]
        tmp_chk_dis = p_in_doc["discharge_pressure"]["check"]
        tmp_chk_del = p_in_doc["delta_pressure"]["check"]
        tmp_chk_flo = p_in_doc["flow"]["check"]
        tmp_chk_amp = p_in_doc["ampere"]["check"]
        tmp_chk_vol = p_in_doc["voltage"]["check"]
        tmp_chk_pfx = p_in_doc["power_factor"]["check"]
        tmp_chk_mot = p_in_doc["motor_efficiency"]["check"]
        tmp_chk_mec = p_in_doc["mechanical_loss"]["check"]
        tmp_chk_spe = p_in_doc["specific_gravity"]["check"]
        tmp_chk_pum = p_in_doc["pump_efficiency"]["check"]

        tmp_chk_in = 0
        tmp_chk_in += (0b100000000000 if tmp_chk_hea == True else 0)
        tmp_chk_in += (0b010000000000 if tmp_chk_suc == True else 0)
        tmp_chk_in += (0b001000000000 if tmp_chk_dis == True else 0)
        tmp_chk_in += (0b000100000000 if tmp_chk_del == True else 0)
        tmp_chk_in += (0b000010000000 if tmp_chk_flo == True else 0)
        tmp_chk_in += (0b000001000000 if tmp_chk_amp == True else 0)
        tmp_chk_in += (0b000000100000 if tmp_chk_vol == True else 0)
        tmp_chk_in += (0b000000010000 if tmp_chk_pfx == True else 0)
        tmp_chk_in += (0b000000001000 if tmp_chk_mot == True else 0)
        tmp_chk_in += (0b000000000100 if tmp_chk_mec == True else 0)
        tmp_chk_in += (0b000000000010 if tmp_chk_spe == True else 0)
        tmp_chk_in += (0b000000000001 if tmp_chk_pum == True else 0)

        tmp_method_arr = [
            0b100010111110, 0b011010111110, 0b000110111110, 0b000011111110, 0b100001111110,
            0b000101111110, 0b011001111110, 0b000001111110, 0b000010111110, 0b100000111110,
            0b000100111110, 0b011000111110, 0b011011111100, 0b000111111100, 0b100011111100,
            0b000011111100, 0b100001111100, 0b011001111100, 0b000101111100, 0b000001111100,
            0b000010111100, 0b100000111100, 0b100011111110, 0b000111111110, 0b011011111110,
            0b000011111111, 0b011001111111, 0b000101111111, 0b100001111111, 0b000001111111,
        ]

        # 해당 계산 번호 찾기
        tmp_idx = 0
        for tmp_method_idx in tmp_method_arr:
            if tmp_chk_in == tmp_method_idx:
                tmp_method_num = tmp_idx + 1
                break

            tmp_idx += 1

        return tmp_method_num

    # =========================================
    # 단위 변경
    # =========================================

    def _to_unit_si_value(self, p_unit_doc: dict, p_unit_category: str, p_unit: str, p_value: float) -> float:
        tmp_unit_key = "{}_{}".format(p_unit_category, p_unit)
        tmp_unit_dict = p_unit_doc[tmp_unit_key]

        _x_ = p_value
        tmp_result = eval(tmp_unit_dict["expr_unit"])

        return tmp_result

    def _to_unit_cust_value(self, p_unit_doc: dict, p_unit_category: str, p_unit: str, p_value: float) -> float:
        tmp_unit_key = "{}_{}".format(p_unit_category, p_unit)
        tmp_unit_dict = p_unit_doc[tmp_unit_key]

        _si_ = p_value
        tmp_result = eval(tmp_unit_dict["expr_si"])

        return tmp_result

    # =========================================
    # 복사
    # =========================================

    def _copy_item_value(self, p_in_doc: dict, p_item_list: list, p_src_item: str, p_dest_item: str, p_is_force_copy: bool) -> None:
        for tmp_item in p_item_list:
            if p_is_force_copy == True:
                p_in_doc[tmp_item][p_dest_item] = p_in_doc[tmp_item][p_src_item]
            else:
                p_in_doc[tmp_item][p_dest_item] = p_in_doc[tmp_item][p_src_item] if p_in_doc[tmp_item][p_dest_item] == None else p_in_doc[tmp_item][p_dest_item]

    # =========================================
    # 곡선 데이터 계산
    # =========================================

    def _fn_head_curve(self, p_curve_doc: dict, p_unit_doc: dict, p_x: float) -> float:
        tmp_x6 = p_curve_doc["head_x6"]
        tmp_x5 = p_curve_doc["head_x5"]
        tmp_x4 = p_curve_doc["head_x4"]
        tmp_x3 = p_curve_doc["head_x3"]
        tmp_x2 = p_curve_doc["head_x2"]
        tmp_x1 = p_curve_doc["head_x1"]
        tmp_x0 = p_curve_doc["head_x0"]

        # x 값을 현재 단위로 변경
        tmp_x = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_flow"]["unit_category"], p_curve_doc["chart_flow"]["unit"], p_x)

        # print("head x: {} => {}".format(p_x, tmp_x))

        # 공식 계산
        tmp_y = tmp_x6 * math.pow(tmp_x, 6) + tmp_x5 * math.pow(tmp_x, 5) + tmp_x4 * math.pow(tmp_x, 4) + tmp_x3 * math.pow(tmp_x, 3) + tmp_x2 * math.pow(tmp_x, 2) + tmp_x1 * math.pow(tmp_x, 1) + tmp_x0

        # y 값을 si 단위로 변경
        tmp_result = self._to_unit_si_value(p_unit_doc, p_curve_doc["chart_head"]["unit_category"], p_curve_doc["chart_head"]["unit"], tmp_y)

        # print("head y: {} => {}".format(tmp_y, tmp_result))

        return tmp_result

    def _fn_pump_efficiency_curve(self, p_curve_doc: dict, p_unit_doc: dict, p_x: float) -> float:
        tmp_x6 = p_curve_doc["efficiency_x6"]
        tmp_x5 = p_curve_doc["efficiency_x5"]
        tmp_x4 = p_curve_doc["efficiency_x4"]
        tmp_x3 = p_curve_doc["efficiency_x3"]
        tmp_x2 = p_curve_doc["efficiency_x2"]
        tmp_x1 = p_curve_doc["efficiency_x1"]
        tmp_x0 = p_curve_doc["efficiency_x0"]

        # x 값을 현재 단위로 변경
        tmp_x = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_flow"]["unit_category"], p_curve_doc["chart_flow"]["unit"], p_x)

        # print("efficiency x: {} => {}".format(p_x, tmp_x))

        # 공식 계산
        tmp_y = tmp_x6 * math.pow(tmp_x, 6) + tmp_x5 * math.pow(tmp_x, 5) + tmp_x4 * math.pow(tmp_x, 4) + tmp_x3 * math.pow(tmp_x, 3) + tmp_x2 * math.pow(tmp_x, 2) + tmp_x1 * math.pow(tmp_x, 1) + tmp_x0

        # y 값을 si 단위로 변경
        tmp_result = self._to_unit_si_value(p_unit_doc, p_curve_doc["chart_efficiency"]["unit_category"], p_curve_doc["chart_efficiency"]["unit"], tmp_y)

        # print("efficiency y: {} => {}".format(tmp_y, tmp_result))

        return tmp_result

    def _fn_shaft_power_curve(self, p_curve_doc: dict, p_unit_doc: dict, p_x: float) -> float:
        tmp_x6 = p_curve_doc["power_x6"]
        tmp_x5 = p_curve_doc["power_x5"]
        tmp_x4 = p_curve_doc["power_x4"]
        tmp_x3 = p_curve_doc["power_x3"]
        tmp_x2 = p_curve_doc["power_x2"]
        tmp_x1 = p_curve_doc["power_x1"]
        tmp_x0 = p_curve_doc["power_x0"]

        # x 값을 현재 단위로 변경
        tmp_x = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_flow"]["unit_category"], p_curve_doc["chart_flow"]["unit"], p_x)

        # print("power x: {} => {}".format(p_x, tmp_x))

        # 공식 계산
        tmp_y = tmp_x6 * math.pow(tmp_x, 6) + tmp_x5 * math.pow(tmp_x, 5) + tmp_x4 * math.pow(tmp_x, 4) + tmp_x3 * math.pow(tmp_x, 3) + tmp_x2 * math.pow(tmp_x, 2) + tmp_x1 * math.pow(tmp_x, 1) + tmp_x0

        # y 값을 si 단위로 변경
        tmp_result = self._to_unit_si_value(p_unit_doc, p_curve_doc["chart_power"]["unit_category"], p_curve_doc["chart_power"]["unit"], tmp_y)

        # print("power y: {} => {}".format(tmp_y, tmp_result))

        return tmp_result

    # =========================================
    # 역함수 곡선 데이터 계산
    # =========================================

    def _inv_fn_head_curve(self, p_curve_doc: dict, p_unit_doc: dict, p_x_min: float, p_x_max: float, p_y: float) -> float:
        tmp_x6 = p_curve_doc["head_x6"]
        tmp_x5 = p_curve_doc["head_x5"]
        tmp_x4 = p_curve_doc["head_x4"]
        tmp_x3 = p_curve_doc["head_x3"]
        tmp_x2 = p_curve_doc["head_x2"]
        tmp_x1 = p_curve_doc["head_x1"]
        tmp_x0 = p_curve_doc["head_x0"]

        # y 값을 현재 단위로 변경
        tmp_y = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_head"]["unit_category"], p_curve_doc["chart_head"]["unit"], p_y)

        tmp_count = 0
        tmp_x_min = p_x_min
        tmp_x_max = p_x_max
        tmp_x_mid = 0
        while True:
            # 최대 loop 수 20
            tmp_count += 1

            # 중간값 계산, 함수 계산
            tmp_x_mid = (tmp_x_min + tmp_x_max) / 2.0
            tmp_cal_y = tmp_x6 * math.pow(tmp_x_mid, 6) + tmp_x5 * math.pow(tmp_x_mid, 5) + tmp_x4 * math.pow(tmp_x_mid, 4) + tmp_x3 * math.pow(tmp_x_mid, 3) + tmp_x2 * math.pow(tmp_x_mid, 2) + tmp_x1 * math.pow(tmp_x_mid, 1) + tmp_x0

            if tmp_cal_y > tmp_y:
                tmp_x_min = tmp_x_mid
            else:
                tmp_x_max = tmp_x_mid

            # 탈출 조건
            if tmp_count > 20 or ((abs(tmp_cal_y) - tmp_y) / (abs(tmp_cal_y)) * 100.0) < 0.1:
                break

        if tmp_count > 20:
            raise Exception("The head value is not exists")

        # x 값을 SI 단위로 변경
        tmp_result = self._to_unit_si_value(p_unit_doc, p_curve_doc["chart_flow"]["unit_category"], p_curve_doc["chart_flow"]["unit"], tmp_x_mid)

        return tmp_result

    def _inv_fn_shaft_power_curve(self, p_curve_doc: dict, p_unit_doc: dict, p_x_min: float, p_x_max: float, p_y: float) -> float:
        tmp_x6 = p_curve_doc["power_x6"]
        tmp_x5 = p_curve_doc["power_x5"]
        tmp_x4 = p_curve_doc["power_x4"]
        tmp_x3 = p_curve_doc["power_x3"]
        tmp_x2 = p_curve_doc["power_x2"]
        tmp_x1 = p_curve_doc["power_x1"]
        tmp_x0 = p_curve_doc["power_x0"]

        # y 값을 현재 단위로 변경
        tmp_y = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_power"]["unit_category"], p_curve_doc["chart_power"]["unit"], p_y)

        tmp_count = 0
        tmp_x_min = p_x_min
        tmp_x_max = p_x_max
        tmp_x_mid = 0
        while True:
            # 최대 loop 수 20
            tmp_count += 1

            # 중간값 계산, 함수 계산
            tmp_x_mid = (tmp_x_min + tmp_x_max) / 2.0
            tmp_cal_y = tmp_x6 * math.pow(tmp_x_mid, 6) + tmp_x5 * math.pow(tmp_x_mid, 5) + tmp_x4 * math.pow(tmp_x_mid, 4) + tmp_x3 * math.pow(tmp_x_mid, 3) + tmp_x2 * math.pow(tmp_x_mid, 2) + tmp_x1 * math.pow(tmp_x_mid, 1) + tmp_x0

            if tmp_cal_y > tmp_y:
                tmp_x_min = tmp_x_mid
            else:
                tmp_x_max = tmp_x_mid

            # 탈출 조건
            if tmp_count > 20 or ((abs(tmp_cal_y) - tmp_y) / (abs(tmp_cal_y)) * 100.0) < 0.1:
                break

        if tmp_count > 20:
            raise Exception("The shaft value is not exists")

        # x 값을 SI 단위로 변경
        tmp_result = self._to_unit_si_value(p_unit_doc, p_curve_doc["chart_flow"]["unit_category"], p_curve_doc["chart_flow"]["unit"], tmp_x_mid)

        return tmp_result

    # =========================================
    # 퍼포먼스 연산 함수
    # =========================================

    def calculate(self, p_curve_doc: dict, p_unit_doc: dict, p_in_doc: dict, p_number_of_decimal_places: int = None) -> dict:
        """PUMP performance 계산

        Args:
            p_curve_doc (dict): curve 정보
                // 입력 정보
                {
                    "head_x6": 0,
                    ...
                    "head_x0": 0,
                    "efficiency_x6": 0,
                    ...
                    "efficiency_x0": 0,
                    "power_x6": 0,
                    ...
                    "power_x0": 0,

                    "x_min": 0,
                    "x_max": 0,

                    "chart_head": { "unit_category" : "c", "unit": "x"},
                    "chart_efficiency": { "unit_category" : "c", "unit": "x"},
                    "chart_power": { "unit_category" : "c", "unit": "x"},
                    "chart_flow": { "unit_category" : "c", "unit": "x"},

                    "db_voltage": 0,
                    "db_power_factor": 0,
                    "db_motor_efficiency": 0,
                    "db_specific_gravity": 0,
                }
            p_unit_doc (dict): unit 정보
                // 입력 정보
                {
                    "head_m": {"unit_expr": "_si_ = _x_", "si_expr" : "_x_ = _si_" }
                    ....
                    "motor_power_x": {"unit_expr": "_si_ = _x_", "si_expr" : "_x_ = _si_" }
                }
            p_in_doc (dict): 입력 정보
                // 입력 정보
                {
                    "head": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "head", "unit": "m"},
                    "suction_pressure": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "discharge_pressure": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "delta_pressure": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "flow": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "ampere": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "voltage": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "power_factor": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "motor_efficiency": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "mechanical_loss": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "specific_gravity": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "pump_efficiency": {"check": {true | flase}, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "hydraulic_power": {"check":false, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "shaft_power": {"check":false, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                    "motor_power": {"check":false, "input" : {0 | None}, "unit_category": "...", "unit": "m"},
                }

        Returns:
            dict: 결과 정보
            {
                    "head": {"input": {0 | None}, "design" : {0 | None}},
                    "suction_pressure": {"input": {0 | None}, "design" : {0 | None}},
                    "discharge_pressure": {"input": {0 | None}, "design" : {0 | None}},
                    "delta_pressure": {"input": {0 | None}, "design" : {0 | None}},
                    "flow": {"input": {0 | None}, "design" : {0 | None}},
                    "ampere": {"input": {0 | None}, "design" : {0 | None}},
                    "voltage": {"input": {0 | None}, "design" : {0 | None}},
                    "power_factor": {"input": {0 | None}, "design" : {0 | None}},
                    "motor_efficiency": {"input": {0 | None}, "design" : {0 | None}},
                    "mechanical_loss": {"input": {0 | None}, "design" : {0 | None}},
                    "specific_gravity": {"input": {0 | None}, "design" : {0 | None}},
                    "pump_efficiency": {"input": {0 | None}, "design" : {0 | None}},
                    "hydraulic_power": {"input": {0 | None}, "design" : {0 | None}},
                    "shaft_power": {"input": {0 | None}, "design" : {0 | None}},
                    "motor_power": {"input": {0 | None}, "design" : {0 | None}},

                    "method" : {None | 0}
                    "current_flow" : {None | 0}
                    "active_head" : {None | 0}
                    "active_pump_efficiency" : {None | 0}
                    "active_shaft_power" : {None | 0}
                    "design_head" : {None | 0}
                    "design_pump_efficiency" : {None | 0}
                    "design_shaft_power" : {None | 0}
                }
        """

        tmp_method_num = 0
        tmp_method_num = self._select_method_num(p_in_doc)
        if tmp_method_num <= 0:
            return {"message": "연산 방법이 존재 하지 않습니다."}

        # 계산을 위한 항목 값 넣기
        tmp_si_data_doc = {}
        for tmp_category in PerformancePump.ALL_ITEMS:
            tmp_si_data_doc[tmp_category] = {
                "si_input": None,
                "si_design": None
            }

            # SI 단위로 변경
            if p_in_doc[tmp_category]["check"] == True and p_in_doc[tmp_category]["input"] != None:
                tmp_si_value = self._to_unit_si_value(p_unit_doc, p_in_doc[tmp_category]["unit_category"], p_in_doc[tmp_category]["unit"], p_in_doc[tmp_category]["input"])
                tmp_si_data_doc[tmp_category]["si_input"] = tmp_si_value
                tmp_si_data_doc[tmp_category]["si_design"] = tmp_si_value

        # DB 단위를 기본 SI 단위로 변경
        p_curve_doc["db_voltage"] = p_curve_doc["db_voltage"]
        p_curve_doc["db_power_factor"] = p_curve_doc["db_power_factor"]
        p_curve_doc["db_motor_efficiency"] = p_curve_doc["db_motor_efficiency"]
        p_curve_doc["db_specific_gravity"] = p_curve_doc["db_specific_gravity"] * 1000

        # print(tmp_si_data_doc)

        # method 호출
        tmp_method_fun = "self._fn_method_{}(p_curve_doc, p_unit_doc, tmp_si_data_doc)".format(tmp_method_num)
        eval(tmp_method_fun)

        # print("result==========================")
        # print(tmp_si_data_doc)

        # 결과 정보 넣기 (input/design)
        tmp_ret_doc = {}
        for tmp_category in PerformancePump.ALL_ITEMS:
            tmp_input = None
            tmp_design = None

            # 요청 단위로 다시 변경
            if p_in_doc[tmp_category]["check"] == True:
                tmp_input = p_in_doc[tmp_category]["input"]
            else:
                tmp_input = None if tmp_si_data_doc[tmp_category]["si_input"] == None else self._to_unit_cust_value(p_unit_doc, p_in_doc[tmp_category]["unit_category"], p_in_doc[tmp_category]["unit"], tmp_si_data_doc[tmp_category]["si_input"])
            tmp_design = None if tmp_si_data_doc[tmp_category]["si_design"] == None else self._to_unit_cust_value(p_unit_doc, p_in_doc[tmp_category]["unit_category"], p_in_doc[tmp_category]["unit"], tmp_si_data_doc[tmp_category]["si_design"])

            # 자릿수 확인
            if p_number_of_decimal_places != None:
                if p_in_doc[tmp_category]["check"] == False:
                    tmp_input = None if tmp_input == None else round(tmp_input, p_number_of_decimal_places)
                tmp_design = None if tmp_design == None else round(tmp_design, p_number_of_decimal_places)

            tmp_ret_doc[tmp_category] = {
                "input": tmp_input,
                "design": tmp_design,
            }

        # 전체적인 결과 넣기 (SI 단위를 cust 단위로 변경)
        # print(p_curve_doc)
        tmp_ret_doc["method_num"] = tmp_method_num
        tmp_ret_doc["current_flow"] = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_flow"]["unit_category"], p_curve_doc["chart_flow"]["unit"], tmp_si_data_doc["flow"]["si_design"])
        tmp_ret_doc["active_head"] = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_head"]["unit_category"], p_curve_doc["chart_head"]["unit"], tmp_si_data_doc["head"]["si_input"])
        tmp_ret_doc["active_pump_efficiency"] = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_efficiency"]["unit_category"], p_curve_doc["chart_efficiency"]["unit"], tmp_si_data_doc["pump_efficiency"]["si_input"])
        tmp_ret_doc["active_shaft_power"] = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_power"]["unit_category"], p_curve_doc["chart_power"]["unit"], tmp_si_data_doc["shaft_power"]["si_input"])
        tmp_ret_doc["design_head"] = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_head"]["unit_category"], p_curve_doc["chart_head"]["unit"], tmp_si_data_doc["head"]["si_design"])
        tmp_ret_doc["design_pump_efficiency"] = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_efficiency"]["unit_category"], p_curve_doc["chart_efficiency"]["unit"], tmp_si_data_doc["pump_efficiency"]["si_design"])
        tmp_ret_doc["design_shaft_power"] = self._to_unit_cust_value(p_unit_doc, p_curve_doc["chart_power"]["unit_category"], p_curve_doc["chart_power"]["unit"], tmp_si_data_doc["shaft_power"]["si_design"])

        # 메세지 넣기
        tmp_ret_doc["message"] = ""

        # print("befor return ==========================")
        # print(tmp_ret_doc)

        return tmp_ret_doc

    # =============================
    # 공식 #1
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_1(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["head", "flow", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = (p_si_data_doc["shaft_power"][tmp_item] / p_si_data_doc["motor_efficiency"][tmp_item]) * (1.0 / (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])
            p_si_data_doc["delta_pressure"][tmp_item] = (p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        print("si_design ==========================")
        print(p_si_data_doc)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["delta_pressure"][tmp_item] = (p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = (p_si_data_doc["shaft_power"][tmp_item] / p_si_data_doc["motor_efficiency"][tmp_item]) * (1.0 / (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        print("si_input ==========================")
        print(p_si_data_doc)

        return None

    # =============================
    # 공식 #2
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_2(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["suction_pressure", "discharge_pressure", "flow", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = (p_si_data_doc["shaft_power"][tmp_item] / p_si_data_doc["motor_efficiency"][tmp_item]) * (1.0 / (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])
            p_si_data_doc["delta_pressure"][tmp_item] = (p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["delta_pressure"][tmp_item] = (p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)
            p_si_data_doc["head"][tmp_item] = ((p_si_data_doc["discharge_pressure"][tmp_item] - p_si_data_doc["suction_pressure"][tmp_item]) / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)) * 9.81
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = (p_si_data_doc["shaft_power"][tmp_item] / p_si_data_doc["motor_efficiency"][tmp_item]) * (1.0 / (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        return None

    # =============================
    # 공식 #3
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_3(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["delta_pressure", "flow", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = (p_si_data_doc["shaft_power"][tmp_item] / p_si_data_doc["motor_efficiency"][tmp_item]) * (1.0 / (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["delta_pressure"][tmp_item] / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)) * 9.81
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = (p_si_data_doc["shaft_power"][tmp_item] / p_si_data_doc["motor_efficiency"][tmp_item]) * (1.0 / (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        return None

    # =============================
    # 공식 #4
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_4(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = (p_si_data_doc["shaft_power"][tmp_item] / p_si_data_doc["motor_efficiency"][tmp_item]) * (1.0 / (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])
            p_si_data_doc["delta_pressure"][tmp_item] = (p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 3.6 * math.pow(10, 6)) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = (p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #5
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_5(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["head", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = (p_si_data_doc["shaft_power"][tmp_item] / p_si_data_doc["motor_efficiency"][tmp_item]) * (1.0 / (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            Q_temp = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, Q_temp)
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["flow"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 3.6 * math.pow(10, 6)) / (p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = (p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #6
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_6(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["delta_pressure", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["delta_pressure"][tmp_item] / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)) * 9.81
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = (p_si_data_doc["shaft_power"][tmp_item] / p_si_data_doc["motor_efficiency"][tmp_item]) * (1.0 / (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            Q_temp = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, Q_temp)
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["delta_pressure"][tmp_item] / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)) * 9.81
            p_si_data_doc["flow"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 3.6 * math.pow(10, 6)) / (p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81)

        return None

    # =============================
    # 공식 #7
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_7(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["suction_pressure", "discharge_pressure", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["delta_pressure"][tmp_item] = p_curve_doc["discharge_pressure"][tmp_item] - p_curve_doc["suction_pressure"][tmp_item]
            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["delta_pressure"][tmp_item] / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)) * 9.81
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = (p_si_data_doc["shaft_power"][tmp_item] / p_si_data_doc["motor_efficiency"][tmp_item]) * (1.0 / (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            Q_temp = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, Q_temp)
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["head"][tmp_item] = ((p_curve_doc["discharge_pressure"][tmp_item] - p_curve_doc["suction_pressure"][tmp_item]) / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)) * 9.81
            p_si_data_doc["flow"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 3.6 * math.pow(10, 6)) / (p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = p_curve_doc["discharge_pressure"][tmp_item] - p_curve_doc["suction_pressure"][tmp_item]

        return None

    # =============================
    # 공식 #8
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_8(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)

        return None

    # =============================
    # 공식 #9
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_9(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["flow", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #10
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_10(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["head", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #11
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_11(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["delta_pressure", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = (p_curve_doc["delta_pressure"][tmp_item] / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)) * 9.81
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["head"][tmp_item] = (p_curve_doc["delta_pressure"][tmp_item] / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)) * 9.81
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        return None

    # =============================
    # 공식 #12
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_12(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["suction_pressure", "discharge_pressure", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = ((p_curve_doc["discharge_pressure"][tmp_item] - p_curve_doc["suction_pressure"][tmp_item]) / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)) * 9.81
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["head"][tmp_item] = ((p_curve_doc["discharge_pressure"][tmp_item] - p_curve_doc["suction_pressure"][tmp_item]) / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)) * 9.81
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])
            p_si_data_doc["delta_pressure"][tmp_item] = p_curve_doc["discharge_pressure"][tmp_item] - p_curve_doc["suction_pressure"][tmp_item]

        return None

    # =============================
    # 공식 #13
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_13(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["suction_pressure", "discharge_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = (3.6 * math.pow(10, 6) * p_si_data_doc["hydraulic_power"][tmp_item]) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = p_curve_doc["discharge_pressure"][tmp_item] - p_curve_doc["suction_pressure"][tmp_item]

        return None

    # =============================
    # 공식 #14
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"
    def _fn_method_14(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = (3.6 * math.pow(10, 6) * p_si_data_doc["hydraulic_power"][tmp_item]) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * 9.81)

        return None

    # =============================
    # 공식 #15
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_15(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["head", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = (3.6 * math.pow(10, 6) * p_si_data_doc["hydraulic_power"][tmp_item]) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #16
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_16(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = (3.6 * math.pow(10, 6) * p_si_data_doc["hydraulic_power"][tmp_item]) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #17
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_17(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["head", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = (3.6 * math.pow(10, 6) * p_si_data_doc["hydraulic_power"][tmp_item]) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #18
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_18(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["suction_pressure", "discharge_pressure", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = (3.6 * math.pow(10, 6) * p_si_data_doc["hydraulic_power"][tmp_item]) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = p_curve_doc["discharge_pressure"][tmp_item] - p_curve_doc["suction_pressure"][tmp_item]

        return None

    # =============================
    # 공식 #19
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_19(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["delta_pressure", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = (3.6 * math.pow(10, 6) * p_si_data_doc["hydraulic_power"][tmp_item]) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * 9.81)

        return None

    # =============================
    # 공식 #20
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_20(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x,  p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = (3.6 * math.pow(10, 6) * p_si_data_doc["hydraulic_power"][tmp_item]) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #21
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_21(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["flow", "voltage", "power_factor", "motor_efficiency", "mechanical_loss"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = (3.6 * math.pow(10, 6) * p_si_data_doc["hydraulic_power"][tmp_item]) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #22
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_22(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["head", "voltage", "power_factor", "motor_efficiency", "mechanical_loss"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["ampere"][tmp_item] = (1000.0 * p_si_data_doc["motor_power"][tmp_item]) / (math.sqrt(3) * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * p_si_data_doc["power_factor"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["specific_gravity"][tmp_item] = (3.6 * math.pow(10, 6) * p_si_data_doc["hydraulic_power"][tmp_item]) / (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * 9.81)
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #23
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_23(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["head", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 100.0) / p_si_data_doc["shaft_power"][tmp_item]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #24
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_24(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["delta_pressure"][tmp_item] * 9.81) / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)
            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 100.0) / p_si_data_doc["shaft_power"][tmp_item]

        return None

    # =============================
    # 공식 #25
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_25(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["suction_pressure", "discharge_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["delta_pressure"][tmp_item] = p_si_data_doc["discharge_pressure"][tmp_item] - p_si_data_doc["suction_pressure"][tmp_item]
            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["delta_pressure"][tmp_item] * 9.81) / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)
            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 100.0) / p_si_data_doc["shaft_power"][tmp_item]

        return None

    # =============================
    # 공식 #26
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_26(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["hydraulic_power"][tmp_item] / (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 100.0) / p_si_data_doc["shaft_power"][tmp_item]
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        return None

    # =============================
    # 공식 #27
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_27(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["suction_pressure", "discharge_pressure", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["delta_pressure"][tmp_item] = p_si_data_doc["discharge_pressure"][tmp_item] - p_si_data_doc["suction_pressure"][tmp_item]
            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["delta_pressure"][tmp_item] * 9.81) / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["delta_pressure"][tmp_item] = p_si_data_doc["discharge_pressure"][tmp_item] - p_si_data_doc["suction_pressure"][tmp_item]
            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["delta_pressure"][tmp_item] * 9.81) / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 100.0) / p_si_data_doc["shaft_power"][tmp_item]

        return None

    # =============================
    # 공식 #28
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_28(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["delta_pressure", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["delta_pressure"][tmp_item] * 9.81) / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["head"][tmp_item] = (p_si_data_doc["delta_pressure"][tmp_item] * 9.81) / (p_si_data_doc["specific_gravity"][tmp_item] / 1000.0)
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 100.0) / p_si_data_doc["shaft_power"][tmp_item]

        return None

    # =============================
    # 공식 #29
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_29(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["head", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["specific_gravity"][tmp_item] = p_curve_doc["db_specific_gravity"]
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["shaft_power"][tmp_item] = self._fn_shaft_power_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["motor_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] / (p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item]))
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["delta_pressure"][tmp_item] = (p_curve_doc["head"][tmp_item] * p_curve_doc["specific_gravity"][tmp_item]) / (9.81 * 1000.0)
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_head_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x, p_si_data_doc["head"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 100.0) / p_si_data_doc["shaft_power"][tmp_item]

        return None

    # =============================
    # 공식 #30
    # =============================
    # "head", "suction_pressure", "discharge_pressure", "delta_pressure", "flow", "ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity", "pump_efficiency", "hydraulic_power", "shaft_power", "motor_power"

    def _fn_method_30(self, p_curve_doc: dict, p_unit_doc: dict, p_si_data_doc: dict) -> None:
        tmp_category_list = ["ampere", "voltage", "power_factor", "motor_efficiency", "mechanical_loss", "specific_gravity"]

        # 역함수를 위한 min/max x 값
        tmp_min_x = p_si_data_doc["x_min"]
        tmp_max_x = p_si_data_doc["x_max"]

        # input 값을 강제로 design 값으로 복사
        self._copy_item_value(p_si_data_doc, tmp_category_list, "si_input", "si_design", True)

        # design 계산
        if True:
            tmp_item = "si_design"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x,  p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["pump_efficiency"][tmp_item] = self._fn_pump_efficiency_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = p_si_data_doc["shaft_power"][tmp_item] * (p_si_data_doc["pump_efficiency"][tmp_item] / 100.0)

        # input 값이 존재 하지 않는 경우 design 값을 input 값으로 복사
        self._copy_item_value(p_si_data_doc, PerformancePump.ALL_ITEMS, "si_design", "si_input", False)

        # active 계산
        if True:
            tmp_item = "si_input"

            p_si_data_doc["motor_power"][tmp_item] = (math.sqrt(3) * p_si_data_doc["ampere"][tmp_item] * p_si_data_doc["voltage"][tmp_item] * p_si_data_doc["power_factor"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item]) / 1000.0
            p_si_data_doc["shaft_power"][tmp_item] = p_si_data_doc["motor_power"][tmp_item] * p_si_data_doc["motor_efficiency"][tmp_item] * (1.0 - p_si_data_doc["mechanical_loss"][tmp_item])
            p_si_data_doc["flow"][tmp_item] = self._inv_fn_shaft_power_curve(p_curve_doc, p_unit_doc, tmp_min_x, tmp_max_x,  p_si_data_doc["shaft_power"][tmp_item])
            p_si_data_doc["head"][tmp_item] = self._fn_head_curve(p_curve_doc, p_unit_doc, p_si_data_doc["flow"][tmp_item])
            p_si_data_doc["hydraulic_power"][tmp_item] = (p_si_data_doc["flow"][tmp_item] * p_si_data_doc["head"][tmp_item] * p_si_data_doc["specific_gravity"][tmp_item] * 9.81) / (3.6 * math.pow(10, 6))
            p_si_data_doc["pump_efficiency"][tmp_item] = (p_si_data_doc["hydraulic_power"][tmp_item] * 100.0) / p_si_data_doc["shaft_power"][tmp_item]

        return None
