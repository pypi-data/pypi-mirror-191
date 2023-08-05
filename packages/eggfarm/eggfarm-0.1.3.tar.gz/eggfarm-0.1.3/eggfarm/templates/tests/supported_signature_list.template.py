from stonewave.sql.udtfs.constants import ParameterDataType as pt
import toml
from pathlib import Path


def _param_to_param_data_type(param):
    # this mandates ParameterDataType to name its attributes the same as the values in info.toml
    return getattr(pt, param)


def _toml_sig_to_params_list(params):
    return [_param_to_param_data_type(param) for param in params]


def supported_signature_list():
    info_toml = Path(__file__).parent.parent / "{{ func_name }}" / "info.toml"
    with open(info_toml, "r") as f:
        info = toml.load(f)
        sigs = [_toml_sig_to_params_list(sig) for sig in info["signature_list"]]
        return sigs
