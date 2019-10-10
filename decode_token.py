from shared import OPAYGOShared
from shared_extended import OPAYGOSharedExtended


class OPAYGODecoder:
    MAX_TOKEN_JUMP = 30
    MAX_TOKEN_JUMP_COUNTER_SYNC = 100

    @classmethod
    def get_activation_value_count_and_type_from_token(cls, token, starting_code, key, last_count,
                                                       restricted_digit_set=False):
        if restricted_digit_set:
            token = OPAYGOShared.convert_from_4_digit_token(token)
        token_base = OPAYGOShared.get_token_base(token) # We get the base of the token
        current_code = OPAYGOShared.put_base_in_token(starting_code, token_base) # We put it into the starting code
        starting_code_base = OPAYGOShared.get_token_base(starting_code) # We get the base of the starting code
        value = cls._decode_base(starting_code_base, token_base)  # If there is a match we get the value from the token
        # We try all combination up until last_count + TOKEN_JUMP, or to the larger jump if syncing counter
        # We could start directly the loop at the last count if we kept the token value for the last count
        if value == OPAYGOShared.COUNTER_SYNC_VALUE:
            max_count_try = last_count + cls.MAX_TOKEN_JUMP_COUNTER_SYNC + 1
        else:
            max_count_try = last_count + cls.MAX_TOKEN_JUMP + 1
        for count in range(0, max_count_try):
            masked_token = OPAYGOShared.put_base_in_token(current_code, token_base)
            if masked_token == token and cls._count_is_valid(count, last_count, value):
                if count % 2:
                    type = OPAYGOShared.TOKEN_TYPE_SET_TIME
                else:
                    type = OPAYGOShared.TOKEN_TYPE_ADD_TIME
                return value, count, type
            current_code = OPAYGOShared.generate_next_token(current_code, key) # If not we go to the next token
        return None, None, None

    @classmethod
    def _count_is_valid(cls, count, last_count, value):
        if value == OPAYGOShared.COUNTER_SYNC_VALUE:
            if count > last_count - 30:
                return True
            else:
                return False
        else:
            if count > last_count:
                return True
            else:
                return False

    @classmethod
    def _decode_base(cls, starting_code_base, token_base):
        decoded_value = token_base - starting_code_base
        if decoded_value < 0:
            return decoded_value + 1000
        else:
            return decoded_value

    @classmethod
    def get_activation_value_count_from_extended_token(cls, token, starting_code, key, last_count,
                                                       restricted_digit_set=False):
        if restricted_digit_set:
            token = OPAYGOSharedExtended.convert_from_4_digit_token(token)
        token_base = OPAYGOSharedExtended.get_token_base(token) # We get the base of the token
        current_code = OPAYGOSharedExtended.put_base_in_token(starting_code, token_base) # We put it into the starting code
        starting_code_base = OPAYGOSharedExtended.get_token_base(starting_code) # We get the base of the starting code
        value = cls._decode_base_extended(starting_code_base, token_base)  # If there is a match we get the value from the token
        for count in range(0, 30):
            masked_token = OPAYGOSharedExtended.put_base_in_token(current_code, token_base)
            if masked_token == token and count > last_count:
                clean_count = count-1
                return value, clean_count
            current_code = OPAYGOSharedExtended.generate_next_token(current_code, key) # If not we go to the next token
        return None, None, None

    @classmethod
    def _decode_base_extended(cls, starting_code_base, token_base):
        decoded_value = token_base - starting_code_base
        if decoded_value < 0:
            return decoded_value + 1000000
        else:
            return decoded_value
