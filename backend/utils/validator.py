from config import Config

class InputValidator:

    @staticmethod
    def validate_d1_input(data):
        errors = []

        if not isinstance(data, dict):
            return False, ["Input must be a JSON object"]

        for feature in Config.D1_FEATURES:
            if feature not in data:
                errors.append(f"Missing field: {feature}")
                continue

            value = data[feature]

            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"{feature} must be a number")
                continue

            if feature in Config.FIELD_RANGES:
                min_val, max_val = Config.FIELD_RANGES[feature]
                if not (min_val <= value <= max_val):
                    errors.append(f"{feature} must be between {min_val} and {max_val}")

        if errors:
            return False, errors

        return True, None

    @staticmethod
    def validate_d2_input(data):
        errors = []

        if not isinstance(data, dict):
            return False, ["Input must be a JSON object"]

        for feature in Config.D2_FEATURES:
            if feature not in data:
                errors.append(f"Missing field: {feature}")
                continue

            value = data[feature]

            if feature == 'Gender':
                if value not in [0, 1]:
                    errors.append("Gender must be 0 or 1")
            elif feature == 'Age':
                if not isinstance(value, (int, float)) or isinstance(value, bool) or not (15 <= value <= 60):
                    errors.append("Age must be between 15 and 60")
            else:
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    errors.append(f"{feature} must be a number")
                elif not (1 <= value <= 5):
                    errors.append(f"{feature} must be between 1 and 5")

        if errors:
            return False, errors

        return True, None
