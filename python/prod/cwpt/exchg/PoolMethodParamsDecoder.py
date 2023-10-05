# PoolMethodParamsDecoder.py
# Author: Ian Moore ( imoore@syscoin.org )
# Original: PoolMethodParamsDecoder class from BalancerPools_Model
# - https://github.com/TokenEngineeringCommunity/BalancerPools_Model
# Date: Sept 2023

from python.prod.cwpt.exchg.amount import TokenAmount
from python.prod.cwpt.exchg.input import JoinParamsInput
from python.prod.cwpt.exchg.input import JoinSwapExternAmountInInput
from python.prod.cwpt.exchg.input import JoinSwapPoolAmountOutInput
from python.prod.cwpt.exchg.input import SwapExactAmountInInput
from python.prod.cwpt.exchg.input import SwapExactAmountOutInput
from python.prod.cwpt.exchg.input import ExitPoolInput
from python.prod.cwpt.exchg.input import ExitSwapPoolAmountInInput
from python.prod.cwpt.exchg.input import ExitSwapPoolExternAmountOutInput
from python.prod.cwpt.exchg.output import JoinParamsOutput
from python.prod.cwpt.exchg.output import JoinSwapExternAmountInOutput
from python.prod.cwpt.exchg.output import JoinSwapPoolAmountOutOutput
from python.prod.cwpt.exchg.output import SwapExactAmountInOutput
from python.prod.cwpt.exchg.output import SwapExactAmountOutOutput
from python.prod.cwpt.exchg.output import ExitPoolOutput
from python.prod.cwpt.exchg.output import ExitSwapPoolAmountInOutput
from python.prod.cwpt.exchg.output import ExitSwapPoolExternAmountOutOutput

class PoolMethodParamsDecoder:

    @staticmethod
    def join_pool_simplified(action: dict) -> (JoinParamsInput, JoinParamsOutput):
        tokens_in = action['tokens_in']
        join_input = JoinParamsInput(Decimal(action['pool_amount_out']), list(filter(lambda x: x['symbol'], tokens_in)))
        join_output = JoinParamsOutput(list(map(lambda x: TokenAmount.ta_with_dict(x), tokens_in)))
        return join_input, join_output

    @staticmethod
    def join_pool_contract_call(action: dict, contract_call: dict) -> (JoinParamsInput, JoinParamsOutput):
        tokens_in = action['tokens_in']
        join_input = JoinParamsInput(Decimal(contract_call['inputs']['poolAmountOut']), list(filter(lambda x: x['symbol'], tokens_in)))
        join_output = JoinParamsOutput(list(map(lambda x: TokenAmount.ta_with_dict(x), tokens_in)))
        return join_input, join_output

    @staticmethod
    def join_swap_extern_amount_in_simplified(action: dict) -> (JoinSwapExternAmountInInput, JoinSwapExternAmountInOutput):
        join_swap_input = JoinSwapExternAmountInInput(TokenAmount.ta_with_dict(action['token_in']))
        join_swap_output = JoinSwapExternAmountInOutput(Decimal(action['pool_amount_out']))
        return join_swap_input, join_swap_output

    @staticmethod
    def join_swap_extern_amount_in_contract_call(action: dict, contract_call: dict) -> (JoinSwapExternAmountInInput, JoinSwapExternAmountInOutput):
        join_swap_input = JoinSwapExternAmountInInput(TokenAmount(symbol=contract_call['inputs']['tokenIn_symbol'], amount=Decimal(contract_call['inputs']['tokenAmountIn'])))
        join_swap_output = JoinSwapExternAmountInOutput(Decimal(action['pool_amount_out']))
        return join_swap_input, join_swap_output

    @staticmethod
    def join_swap_pool_amount_out_contract_call(action: dict, contract_call: dict) -> (JoinSwapPoolAmountOutInput, JoinSwapPoolAmountOutOutput):
        # TODO
        pass

    @staticmethod
    def swap_exact_amount_in_simplified(action: dict) -> (SwapExactAmountInInput, SwapExactAmountInOutput):
        swap_input = SwapExactAmountInInput(token_in=TokenAmount.ta_with_dict(action['token_in']), min_token_out=TokenAmount.ta_with_dict(action['token_out']))
        swap_output = SwapExactAmountInOutput(TokenAmount.ta_with_dict(action['token_out']))
        return swap_input, swap_output

    @staticmethod
    def swap_exact_amount_in_contract_call(action: dict, contract_call: dict) -> (SwapExactAmountInInput, SwapExactAmountInOutput):
        token_in = TokenAmount(symbol=contract_call['inputs']['tokenIn_symbol'], amount=Decimal(contract_call['inputs']['tokenAmountIn']))
        min_token_out = TokenAmount(symbol=contract_call['inputs']['tokenOut_symbol'], amount=Decimal(contract_call['inputs']['minAmountOut']))
        swap_input = SwapExactAmountInInput(token_in=token_in,
                                            min_token_out=min_token_out)
        swap_output = SwapExactAmountInOutput(TokenAmount.ta_with_dict(action['token_out']))
        return swap_input, swap_output

    @staticmethod
    def swap_exact_amount_out_contract_call(action: dict, contract_call: dict) -> (SwapExactAmountOutInput, SwapExactAmountOutOutput):
        max_token_in = TokenAmount(symbol=contract_call['inputs']['tokenIn_symbol'], amount=Decimal(contract_call['inputs']['maxAmountIn']))
        token_out = TokenAmount(symbol=contract_call['inputs']['tokenOut_symbol'], amount=Decimal(contract_call['inputs']['tokenAmountOut']))
        swap_input = SwapExactAmountOutInput(max_token_in=max_token_in, token_out=token_out)
        swap_output = SwapExactAmountOutOutput(TokenAmount.ta_with_dict(action['token_in']))
        return swap_input, swap_output

    @staticmethod
    def exit_pool_simplified(action: dict) -> (ExitPoolInput, ExitPoolOutput):
        exit_input = ExitPoolInput(Decimal(action['pool_amount_in']))
        exit_output = ExitPoolOutput(list(map(lambda x: TokenAmount.ta_with_dict(x), action['tokens_out'])))
        return exit_input, exit_output

    @staticmethod
    def exit_pool_contract_call(action: dict, contract_call: dict) -> (ExitPoolInput, ExitPoolOutput):
        exit_input = ExitPoolInput(Decimal(contract_call['inputs']['poolAmountIn']))
        exit_output = ExitPoolOutput(list(map(lambda x: TokenAmount.ta_with_dict(x), action['tokens_out'])))
        return exit_input, exit_output

    @staticmethod
    def exit_swap_pool_amount_in_simplified(action: dict) -> (ExitSwapPoolAmountInInput, ExitSwapPoolAmountInOutput):
        exit_swap_input = ExitSwapPoolAmountInInput(Decimal(action['pool_amount_in']))
        exit_swap_output = ExitSwapPoolAmountInOutput(token_out=TokenAmount.ta_with_dict(action['token_out']))
        return exit_swap_input, exit_swap_output

    @staticmethod
    def exit_swap_pool_amount_in_contract_call(action: dict, contract_call: dict) -> (ExitSwapPoolAmountInInput, ExitSwapPoolAmountInOutput):
        exit_swap_input = ExitSwapPoolAmountInInput(Decimal(contract_call['inputs']['poolAmountIn']))
        exit_swap_output = ExitSwapPoolAmountInOutput(token_out=TokenAmount.ta_with_dict(action['token_out']))
        return exit_swap_input, exit_swap_output

    @staticmethod
    def exit_swap_extern_amount_out_contract_call(action: dict, contract_call: dict) -> (ExitSwapPoolExternAmountOutInput, ExitSwapPoolExternAmountOutOutput):
        token_out = TokenAmount(symbol=contract_call['inputs']['tokenOut_symbol'], amount=Decimal(contract_call['inputs']['tokenAmountOut']))
        exit_swap_input = ExitSwapPoolExternAmountOutInput(token_out=token_out, max_pool_in=Decimal(contract_call['inputs']['maxPoolAmountIn']))
        exit_swap_output = ExitSwapPoolExternAmountOutOutput(Decimal(action['pool_amount_in']))
        return exit_swap_input, exit_swap_output
