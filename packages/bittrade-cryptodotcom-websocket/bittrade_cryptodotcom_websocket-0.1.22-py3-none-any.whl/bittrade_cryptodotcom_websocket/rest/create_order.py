from typing import Any, Callable, Optional
from ..connection import wait_for_response
from ..models import (
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    CryptodotcomRequestMessage,
    EnhancedWebsocketBehaviorSubject,
)
from elm_framework_helpers.output import debug_operator
from reactivex import Observable, operators, disposable, just, throw
from ..events import MethodName
from ccxt import cryptocom
from reactivex.scheduler import NewThreadScheduler


def order_confirmation(
    messages: Observable[CryptodotcomResponseMessage],
    exchange: cryptocom,
    order_id: str,
):
    def is_match(message: CryptodotcomResponseMessage) -> bool:
        try:
            return message.result["data"][0]["order_id"] == order_id
        except:
            return False

    return messages.pipe(
        operators.filter(is_match),
        operators.take(1),
        operators.map(lambda x: (exchange.parse_order(x.result["data"][0]))),
        operators.flat_map(
            lambda x: just(x) if x["status"] == "open" else throw(x["status"])
        ),
        operators.timeout(4.0),
    )


def create_order_factory(
    messages: Observable[CryptodotcomResponseMessage],
    exchange: cryptocom,
    socket: EnhancedWebsocketBehaviorSubject,
) -> Callable[
    [str, str, str, float, Optional[float], Optional[Any]], Observable[dict[str, Any]]
]:
    """Factory for create order API call

    Args:
        messages (Observable[CryptodotcomResponseMessage]): All messages
        exchange (cryptocom): CCXT exchange
        socket (EnhancedWebsocketBehaviorSubject): Socket behavior subject

    Returns:
        Callable[ [str, str, str, float, Optional[float], Optional[Any]], Observable[dict[str, Any]] ]: Arguments for the returned function are:

        symbol: str,
        type: str,
        side: str,
        amount: float,
        price: Optional[float]=None,
        params=None,
    """

    def create_order(
        symbol: str,
        type: str,
        side: str,
        amount: float,
        price: Optional[float] = None,
        params: Optional[dict[str, Any]] = None,
    ):
        """Create order

        Args:
            symbol (str):
            type (str):
            side (str): buy or sell
            amount (float): amount
            price (Optional[float], optional): price. Defaults to None.
            params (_type_, optional): _description_. Defaults to None.

        Returns:
            dict: Order per CCXT style
        """
        params = params or {}
        market = exchange.market(symbol)
        uppercaseType = type.upper()
        instrument_name = market["id"]
        request = {
            "instrument_name": instrument_name,
            "side": side.upper(),
            "type": uppercaseType,
            "quantity": exchange.amount_to_precision(symbol, amount),
        }
        if params.get("client_oid"):
            request["client_oid"] = params["client_oid"]
        if (uppercaseType == "LIMIT") or (uppercaseType == "STOP_LIMIT"):
            request["price"] = exchange.price_to_precision(symbol, price)
        postOnly = exchange.safe_value(params, "postOnly", False)
        if postOnly:
            request["exec_inst"] = "POST_ONLY"

        def subscribe(observer, scheduler=None):
            recorded_messages = messages.pipe(
                operators.filter(
                    lambda x: (
                        x.result.get("channel") == f"user.order.{instrument_name}"
                    )
                ),
                debug_operator(
                    f"Recorded messages for {params.get('client_oid')}", __name__
                ),
                operators.replay(),
            )
            sub = recorded_messages.connect(scheduler=NewThreadScheduler())
            message_id, sender = socket.value.request_to_observable(
                CryptodotcomRequestMessage(MethodName.CREATE_ORDER, params=request)
            )

            return disposable.CompositeDisposable(
                sub,
                messages.pipe(
                    wait_for_response(
                        message_id,
                        sender,
                        3.0,
                    ),
                    operators.flat_map(
                        lambda x: just(x.result) if x.code == 0 else throw(x.message)
                    ),
                    operators.flat_map(
                        lambda x: order_confirmation(
                            recorded_messages, exchange, x["order_id"]
                        )
                    ),
                ).subscribe(observer, scheduler=scheduler),
            )

        return Observable(subscribe)

    return create_order
