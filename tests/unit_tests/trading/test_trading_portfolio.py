# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2020 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

from decimal import Decimal
import unittest

from nautilus_trader.backtest.loaders import InstrumentLoader
from nautilus_trader.common.clock import TestClock
from nautilus_trader.common.factories import OrderFactory
from nautilus_trader.common.logging import TestLogger
from nautilus_trader.core.uuid import uuid4
from nautilus_trader.data.cache import DataCache
from nautilus_trader.model.currencies import BTC
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.events import AccountState
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import PositionId
from nautilus_trader.model.identifiers import StrategyId
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.identifiers import TraderId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity
from nautilus_trader.model.position import Position
from nautilus_trader.model.tick import QuoteTick
from nautilus_trader.trading.account import Account
from nautilus_trader.trading.portfolio import Portfolio
from nautilus_trader.trading.portfolio import PortfolioFacade
from tests.test_kit.stubs import TestStubs
from tests.test_kit.stubs import UNIX_EPOCH


FXCM = Venue("FXCM")
BINANCE = Venue("BINANCE")
BITMEX = Venue("BITMEX")

AUDUSD_FXCM = InstrumentLoader.default_fx_ccy(Symbol("AUD/USD", Venue("FXCM")))
GBPUSD_FXCM = InstrumentLoader.default_fx_ccy(Symbol("GBP/USD", Venue("FXCM")))
USDJPY_FXCM = InstrumentLoader.default_fx_ccy(Symbol("USD/JPY", Venue("FXCM")))
BTCUSDT_BINANCE = InstrumentLoader.btcusdt_binance()
BTCUSD_BITMEX = InstrumentLoader.xbtusd_bitmex(leverage=Decimal("10.0"))
ETHUSD_BITMEX = InstrumentLoader.ethusd_bitmex(leverage=Decimal("10.0"))


class PortfolioFacadeTests(unittest.TestCase):

    def test_account_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.account, FXCM)

    def test_order_margin_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.order_margin, FXCM)

    def test_position_margin_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.position_margin, FXCM)

    def test_unrealized_pnl_for_venue_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.unrealized_pnl_for_venue, FXCM)

    def test_unrealized_pnl_for_symbol_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.unrealized_pnl_for_symbol, BTCUSDT_BINANCE.symbol)

    def test_open_value_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.open_value, BITMEX)

    def test_net_position_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.net_position, GBPUSD_FXCM.symbol)

    def test_is_net_long_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.is_net_long, GBPUSD_FXCM.symbol)

    def test_is_net_short_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.is_net_short, GBPUSD_FXCM.symbol)

    def test_is_flat_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.is_flat, GBPUSD_FXCM.symbol)

    def test_is_completely_flat_raises_not_implemented_error(self):
        # Arrange
        portfolio = PortfolioFacade()

        # Act
        # Assert
        self.assertRaises(NotImplementedError, portfolio.is_completely_flat)


class PortfolioTests(unittest.TestCase):

    def setUp(self):
        # Fixture Setup
        clock = TestClock()
        logger = TestLogger(clock)
        self.order_factory = OrderFactory(
            trader_id=TraderId("TESTER", "000"),
            strategy_id=StrategyId("S", "001"),
            clock=TestClock(),
        )

        state = AccountState(
            AccountId.from_str("BINANCE-1513111-SIMULATED"),
            BTC,
            Money(10., BTC),
            Money(0., BTC),
            Money(0., BTC),
            uuid4(),
            UNIX_EPOCH
        )

        self.data_cache = DataCache(logger)
        self.account = Account(state)

        self.portfolio = Portfolio(clock, logger)
        self.portfolio.register_account(self.account)
        self.portfolio.register_cache(self.data_cache)

        self.data_cache.add_instrument(AUDUSD_FXCM)
        self.data_cache.add_instrument(GBPUSD_FXCM)
        self.data_cache.add_instrument(BTCUSDT_BINANCE)
        self.data_cache.add_instrument(BTCUSD_BITMEX)
        self.data_cache.add_instrument(ETHUSD_BITMEX)

    def test_account_when_no_account_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertIsNone(self.portfolio.account(FXCM))

    def test_account_when_account_returns_the_account_facade(self):
        # Arrange
        # Act
        result = self.portfolio.account(BINANCE)

        # Assert
        self.assertEqual(self.account, result)

    def test_net_position_when_no_positions_returns_zero(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(Decimal(0), self.portfolio.net_position(AUDUSD_FXCM.symbol))

    def test_is_net_long_when_no_positions_returns_false(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(False, self.portfolio.is_net_long(AUDUSD_FXCM.symbol))

    def test_is_net_short_when_no_positions_returns_false(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(False, self.portfolio.is_net_short(AUDUSD_FXCM.symbol))

    def test_is_flat_when_no_positions_returns_true(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(True, self.portfolio.is_flat(AUDUSD_FXCM.symbol))

    def test_is_completely_flat_when_no_positions_returns_true(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(True, self.portfolio.is_flat(AUDUSD_FXCM.symbol))

    def test_unrealized_pnl_for_symbol_when_no_instrument_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertIsNone(self.portfolio.unrealized_pnl_for_symbol(USDJPY_FXCM.symbol))

    def test_unrealized_pnl_for_venue_when_no_account_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertIsNone(self.portfolio.unrealized_pnl_for_venue(FXCM))

    def test_order_margin_when_no_account_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertIsNone(self.portfolio.order_margin(FXCM))

    def test_position_margin_when_no_account_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertIsNone(self.portfolio.position_margin(FXCM))

    def test_open_value_when_no_account_returns_none(self):
        # Arrange
        # Act
        # Assert
        self.assertIsNone(self.portfolio.open_value(FXCM))

    def test_update_tick(self):
        # Arrange
        tick = TestStubs.quote_tick_5decimal(GBPUSD_FXCM.symbol)

        # Act
        self.portfolio.update_tick(tick)

        # Assert
        self.assertIsNone(self.portfolio.unrealized_pnl_for_symbol(GBPUSD_FXCM.symbol))

    def test_update_orders_working(self):
        # Arrange
        self.portfolio.register_account(self.account)

        # Create two working orders
        order1 = self.order_factory.stop_market(
            BTCUSDT_BINANCE.symbol,
            OrderSide.BUY,
            Quantity("10.5"),
            Price("25000.00"),
        )

        order2 = self.order_factory.stop_market(
            BTCUSDT_BINANCE.symbol,
            OrderSide.BUY,
            Quantity("10.5"),
            Price("25000.00"),
        )

        filled1 = TestStubs.event_order_filled(
            order1,
            instrument=BTCUSDT_BINANCE,
            position_id=PositionId("P-1"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("25000.00"),
        )

        filled2 = TestStubs.event_order_filled(
            order2,
            instrument=BTCUSDT_BINANCE,
            position_id=PositionId("P-2"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("25000.00"),
        )

        # Push state to WORKING
        order1.apply(TestStubs.event_order_submitted(order1))
        order1.apply(TestStubs.event_order_accepted(order1))
        order1.apply(filled1)

        # Push state to WORKING
        order2.apply(TestStubs.event_order_submitted(order2))
        order2.apply(TestStubs.event_order_accepted(order2))
        order2.apply(filled2)

        # Update the last quote
        last = QuoteTick(
            BTCUSDT_BINANCE.symbol,
            Price("25001.00"),
            Price("25002.00"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        # Act
        self.portfolio.update_tick(last)
        self.portfolio.update_orders_working({order1, order2})

        # Assert
        self.assertEqual(Money(0, BTC), self.portfolio.order_margin(BINANCE))

    def test_update_positions(self):
        # Arrange
        self.portfolio.register_account(self.account)

        # Create a closed position
        order1 = self.order_factory.market(
            BTCUSDT_BINANCE.symbol,
            OrderSide.BUY,
            Quantity("10.50000000"),
        )

        order2 = self.order_factory.market(
            BTCUSDT_BINANCE.symbol,
            OrderSide.SELL,
            Quantity("10.50000000"),
        )

        filled1 = TestStubs.event_order_filled(
            order1,
            instrument=BTCUSDT_BINANCE,
            position_id=PositionId("P-1"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("25000.00"),
        )

        filled2 = TestStubs.event_order_filled(
            order2,
            instrument=BTCUSDT_BINANCE,
            position_id=PositionId("P-1"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("25000.00"),
        )

        position1 = Position(filled1)
        position1.apply(filled2)

        order3 = self.order_factory.market(
            BTCUSDT_BINANCE.symbol,
            OrderSide.BUY,
            Quantity("10.00000000"),
        )

        filled3 = TestStubs.event_order_filled(
            order3,
            instrument=BTCUSDT_BINANCE,
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("25000.00"),
        )

        position2 = Position(filled3)

        # Update the last quote
        last = QuoteTick(
            BTCUSDT_BINANCE.symbol,
            Price("25001.00"),
            Price("25002.00"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        # Act
        self.portfolio.update_positions({position1, position2})
        self.portfolio.update_tick(last)

        # Assert
        self.assertTrue(self.portfolio.is_net_long(BTCUSDT_BINANCE.symbol))

    def test_opening_one_long_position_updates_portfolio(self):
        # Arrange
        order = self.order_factory.market(
            BTCUSDT_BINANCE.symbol,
            OrderSide.BUY,
            Quantity("10.000000"),
        )

        fill = TestStubs.event_order_filled(
            order=order,
            instrument=BTCUSDT_BINANCE,
            position_id=PositionId("P-123456"),
            strategy_id=StrategyId("S", "001"),
            fill_price=Price("10500.00"),
        )

        last = QuoteTick(
            BTCUSDT_BINANCE.symbol,
            Price("10500.05"),
            Price("10501.51"),
            Quantity("2.540000"),
            Quantity("0.910000"),
            UNIX_EPOCH,
        )

        self.data_cache.add_quote_tick(last)
        self.portfolio.update_tick(last)

        position = Position(fill)

        # Act
        self.portfolio.update_position(TestStubs.event_position_opened(position))

        # Assert
        self.assertEqual(Money(10., BTC), self.portfolio.open_value(BINANCE))
        self.assertEqual(Money(0, BTC), self.portfolio.position_margin(BINANCE))
        self.assertEqual(Money(0.00004762, BTC), self.portfolio.unrealized_pnl_for_venue(BINANCE))
        self.assertEqual(Money(0.00004762, BTC), self.portfolio.unrealized_pnl_for_symbol(BTCUSDT_BINANCE.symbol))
        self.assertEqual(Decimal(10), self.portfolio.net_position(order.symbol))
        self.assertTrue(self.portfolio.is_net_long(order.symbol))
        self.assertFalse(self.portfolio.is_net_short(order.symbol))
        self.assertFalse(self.portfolio.is_flat(order.symbol))
        self.assertFalse(self.portfolio.is_completely_flat())

    def test_opening_one_short_position_updates_portfolio(self):
        # Arrange
        order = self.order_factory.market(
            BTCUSDT_BINANCE.symbol,
            OrderSide.SELL,
            Quantity("0.515"),
        )

        fill = TestStubs.event_order_filled(
            order=order,
            instrument=BTCUSDT_BINANCE,
            position_id=PositionId("P-123456"),
            strategy_id=StrategyId("S", "001"),
            fill_price=Price("15000.00")
        )

        last = QuoteTick(
            BTCUSDT_BINANCE.symbol,
            Price("15510.15"),
            Price("15510.25"),
            Quantity("12.62"),
            Quantity("3.1"),
            UNIX_EPOCH,
        )

        self.data_cache.add_quote_tick(last)
        self.portfolio.update_tick(last)

        position = Position(fill)

        # Act
        self.portfolio.update_position(TestStubs.event_position_opened(position))

        # Assert
        self.assertEqual(Money(0.51500000, BTC), self.portfolio.open_value(BINANCE))
        self.assertEqual(Money(0, BTC), self.portfolio.position_margin(BINANCE))
        self.assertEqual(Money(-0.01694226, BTC), self.portfolio.unrealized_pnl_for_venue(BINANCE))
        self.assertEqual(Money(-0.01694226, BTC), self.portfolio.unrealized_pnl_for_symbol(BTCUSDT_BINANCE.symbol))
        self.assertEqual(Decimal("-0.515"), self.portfolio.net_position(order.symbol))
        self.assertFalse(self.portfolio.is_net_long(order.symbol))
        self.assertTrue(self.portfolio.is_net_short(order.symbol))
        self.assertFalse(self.portfolio.is_flat(order.symbol))
        self.assertFalse(self.portfolio.is_completely_flat())

    def test_opening_one_position_when_account_in_different_base(self):
        # Arrange
        state = AccountState(
            AccountId.from_str("BITMEX-01234-SIMULATED"),
            BTC,
            Money(10., BTC),
            Money(0., BTC),
            Money(0., BTC),
            uuid4(),
            UNIX_EPOCH,
        )

        account = Account(state)

        self.portfolio.register_account(account)

        last_ethusd = QuoteTick(
            ETHUSD_BITMEX.symbol,
            Price("376.05"),
            Price("377.10"),
            Quantity("16"),
            Quantity("25"),
            UNIX_EPOCH,
        )

        last_btcusd = QuoteTick(
            BTCUSD_BITMEX.symbol,
            Price("10500.05"),
            Price("10501.51"),
            Quantity("2.54"),
            Quantity("0.91"),
            UNIX_EPOCH,
        )

        self.data_cache.add_quote_tick(last_ethusd)
        self.data_cache.add_quote_tick(last_btcusd)
        self.portfolio.update_tick(last_ethusd)
        self.portfolio.update_tick(last_btcusd)

        order = self.order_factory.market(
            ETHUSD_BITMEX.symbol,
            OrderSide.BUY,
            Quantity(10000),
        )

        fill = TestStubs.event_order_filled(
            order=order,
            instrument=ETHUSD_BITMEX,
            position_id=PositionId("P-123456"),
            strategy_id=StrategyId("S", "001"),
            fill_price=Price("376.05"),
            xrate=Decimal("0.0365"),
        )

        position = Position(fill)

        # Act
        self.portfolio.update_position(TestStubs.event_position_opened(position))

        # Assert
        self.assertEqual(Money(0.95237642, BTC), self.portfolio.open_value(BITMEX))
        self.assertEqual(Money(0.00138095, BTC), self.portfolio.position_margin(BITMEX))
        self.assertEqual(Money(0, BTC), self.portfolio.unrealized_pnl_for_venue(BITMEX))
        self.assertEqual(Money(0, BTC), self.portfolio.unrealized_pnl_for_symbol(BTCUSD_BITMEX.symbol))

    def test_unrealized_pnl_when_insufficient_data_for_xrate_returns_none(self):
        # Arrange
        state = AccountState(
            AccountId.from_str("BITMEX-01234-SIMULATED"),
            BTC,
            Money(10., BTC),
            Money(0., BTC),
            Money(0., BTC),
            uuid4(),
            UNIX_EPOCH,
        )

        account = Account(state)

        self.portfolio.register_account(account)
        order = self.order_factory.market(
            ETHUSD_BITMEX.symbol,
            OrderSide.BUY,
            Quantity(100),
        )

        fill = TestStubs.event_order_filled(
            order=order,
            instrument=ETHUSD_BITMEX,
            position_id=PositionId("P-123456"),
            strategy_id=StrategyId("S", "001"),
            fill_price=Price("376.05"),
            xrate=Decimal("0.03776")
        )

        position = Position(fill)

        self.portfolio.update_position(TestStubs.event_position_opened(position))

        # Act
        result = self.portfolio.unrealized_pnl_for_venue(BITMEX)

        # # Assert
        self.assertIsNone(result)

    def test_open_value_when_insufficient_data_for_xrate_returns_none(self):
        # Arrange
        state = AccountState(
            AccountId.from_str("BITMEX-01234-SIMULATED"),
            BTC,
            Money(10., BTC),
            Money(0., BTC),
            Money(0., BTC),
            uuid4(),
            UNIX_EPOCH,
        )

        account = Account(state)

        self.portfolio.register_account(account)

        order = self.order_factory.market(
            ETHUSD_BITMEX.symbol,
            OrderSide.BUY,
            Quantity(100),
        )

        fill = TestStubs.event_order_filled(
            order=order,
            instrument=ETHUSD_BITMEX,
            position_id=PositionId("P-123456"),
            strategy_id=StrategyId("S", "001"),
            fill_price=Price("376.05"),
            xrate=Decimal("0.0378")
        )

        last_ethusd = QuoteTick(
            ETHUSD_BITMEX.symbol,
            Price("376.05"),
            Price("377.10"),
            Quantity("16"),
            Quantity("25"),
            UNIX_EPOCH,
        )

        position = Position(fill)

        self.portfolio.update_position(TestStubs.event_position_opened(position))
        self.data_cache.add_quote_tick(last_ethusd)
        self.portfolio.update_tick(last_ethusd)

        # Act
        result = self.portfolio.open_value(BITMEX)

        # Assert
        self.assertEqual(None, result)

    def test_opening_several_positions_updates_portfolio(self):
        # Arrange
        state = AccountState(
            AccountId.from_str("FXCM-01234-SIMULATED"),
            USD,
            Money(1000000, USD),
            Money(0., USD),
            Money(0., USD),
            uuid4(),
            UNIX_EPOCH,
        )

        account = Account(state)

        self.portfolio.register_account(account)

        last_audusd = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("0.80501"),
            Price("0.80505"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        last_gbpusd = QuoteTick(
            GBPUSD_FXCM.symbol,
            Price("1.30315"),
            Price("1.30317"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.data_cache.add_quote_tick(last_audusd)
        self.data_cache.add_quote_tick(last_gbpusd)
        self.portfolio.update_tick(last_audusd)
        self.portfolio.update_tick(last_gbpusd)

        order1 = self.order_factory.market(
            AUDUSD_FXCM.symbol,
            OrderSide.BUY,
            Quantity(100000),
        )

        order2 = self.order_factory.market(
            GBPUSD_FXCM.symbol,
            OrderSide.BUY,
            Quantity(100000),
        )

        order1_filled = TestStubs.event_order_filled(
            order1,
            instrument=AUDUSD_FXCM,
            position_id=PositionId("P-1"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("1.00000"),
        )

        order2_filled = TestStubs.event_order_filled(
            order2,
            instrument=AUDUSD_FXCM,
            position_id=PositionId("P-2"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("1.00000"),
        )

        position1 = Position(order1_filled)
        position2 = Position(order2_filled)
        position_opened1 = TestStubs.event_position_opened(position1)
        position_opened2 = TestStubs.event_position_opened(position2)

        # Act
        self.portfolio.update_position(position_opened1)
        self.portfolio.update_position(position_opened2)

        # Assert
        self.assertEqual(Money(10816.00, USD), self.portfolio.unrealized_pnl_for_venue(FXCM))
        self.assertEqual(Money(210816.00, USD), self.portfolio.open_value(FXCM))
        self.assertEqual(Money(0., BTC), self.portfolio.unrealized_pnl_for_venue(BINANCE))
        self.assertEqual(Money(0., BTC), self.portfolio.open_value(BINANCE))
        self.assertEqual(Decimal(100000), self.portfolio.net_position(AUDUSD_FXCM.symbol))
        self.assertTrue(self.portfolio.is_net_long(AUDUSD_FXCM.symbol))
        self.assertFalse(self.portfolio.is_net_short(AUDUSD_FXCM.symbol))
        self.assertFalse(self.portfolio.is_flat(AUDUSD_FXCM.symbol))
        self.assertFalse(self.portfolio.is_completely_flat())

    def test_modifying_position_updates_portfolio(self):
        # Arrange
        state = AccountState(
            AccountId.from_str("FXCM-01234-SIMULATED"),
            USD,
            Money(1000000, USD),
            Money(0., USD),
            Money(0., USD),
            uuid4(),
            UNIX_EPOCH,
        )

        account = Account(state)

        self.portfolio.register_account(account)

        last_audusd = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("0.80501"),
            Price("0.80505"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.data_cache.add_quote_tick(last_audusd)
        self.portfolio.update_tick(last_audusd)

        order1 = self.order_factory.market(
            AUDUSD_FXCM.symbol,
            OrderSide.BUY,
            Quantity(100000),
        )

        order1_filled = TestStubs.event_order_filled(
            order1,
            instrument=AUDUSD_FXCM,
            position_id=PositionId("P-123456"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("1.00000"),
        )

        position = Position(order1_filled)

        self.portfolio.update_position(TestStubs.event_position_opened(position))

        order2 = self.order_factory.market(
            AUDUSD_FXCM.symbol,
            OrderSide.SELL,
            Quantity(50000),
        )

        order2_filled = TestStubs.event_order_filled(
            order2,
            instrument=AUDUSD_FXCM,
            position_id=PositionId("P-123456"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("1.00000"),
        )

        position.apply(order2_filled)

        # Act
        self.portfolio.update_position(TestStubs.event_position_modified(position))

        # Assert
        self.assertEqual(Money(-9749.50, USD), self.portfolio.unrealized_pnl_for_venue(FXCM))
        self.assertEqual(Money(40250.50, USD), self.portfolio.open_value(FXCM))
        self.assertEqual(Money(0., BTC), self.portfolio.unrealized_pnl_for_venue(BINANCE))
        self.assertEqual(Money(0., BTC), self.portfolio.open_value(BINANCE))
        self.assertEqual(Decimal(50000), self.portfolio.net_position(AUDUSD_FXCM.symbol))

    def test_closing_position_updates_portfolio(self):
        # Arrange
        state = AccountState(
            AccountId.from_str("FXCM-01234-SIMULATED"),
            USD,
            Money(1000000, USD),
            Money(0., USD),
            Money(0., USD),
            uuid4(),
            UNIX_EPOCH,
        )

        account = Account(state)

        self.portfolio.register_account(account)

        order1 = self.order_factory.market(
            AUDUSD_FXCM.symbol,
            OrderSide.BUY,
            Quantity(100000),
        )

        order1_filled = TestStubs.event_order_filled(
            order1,
            instrument=AUDUSD_FXCM,
            position_id=PositionId("P-123456"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("1.00000"),
        )

        position = Position(order1_filled)

        self.portfolio.update_position(TestStubs.event_position_opened(position))

        order2 = self.order_factory.market(
            AUDUSD_FXCM.symbol,
            OrderSide.SELL,
            Quantity(100000),
        )

        order2_filled = TestStubs.event_order_filled(
            order2,
            instrument=AUDUSD_FXCM,
            position_id=PositionId("P-123456"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("1.00010"),
        )

        position.apply(order2_filled)

        # Act
        self.portfolio.update_position(TestStubs.event_position_closed(position))

        # Assert
        self.assertEqual(Money(0, USD), self.portfolio.unrealized_pnl_for_venue(FXCM))
        self.assertEqual(Money(0, USD), self.portfolio.open_value(FXCM))
        self.assertEqual(Money(0, BTC), self.portfolio.unrealized_pnl_for_venue(BINANCE))
        self.assertEqual(Money(0, BTC), self.portfolio.open_value(BINANCE))
        self.assertEqual(Decimal(0), self.portfolio.net_position(AUDUSD_FXCM.symbol))
        self.assertFalse(self.portfolio.is_net_long(AUDUSD_FXCM.symbol))
        self.assertFalse(self.portfolio.is_net_short(AUDUSD_FXCM.symbol))
        self.assertTrue(self.portfolio.is_flat(AUDUSD_FXCM.symbol))
        self.assertTrue(self.portfolio.is_completely_flat())

    def test_several_positions_with_different_symbols_updates_portfolio(self):
        # Arrange
        state = AccountState(
            AccountId.from_str("FXCM-01234-SIMULATED"),
            USD,
            Money(1000000, USD),
            Money(0., USD),
            Money(0., USD),
            uuid4(),
            UNIX_EPOCH,
        )

        account = Account(state)

        self.portfolio.register_account(account)

        order1 = self.order_factory.market(
            AUDUSD_FXCM.symbol,
            OrderSide.BUY,
            Quantity(100000),
        )

        order2 = self.order_factory.market(
            AUDUSD_FXCM.symbol,
            OrderSide.BUY,
            Quantity(100000),
        )

        order3 = self.order_factory.market(
            GBPUSD_FXCM.symbol,
            OrderSide.BUY,
            Quantity(100000),
        )

        order4 = self.order_factory.market(
            GBPUSD_FXCM.symbol,
            OrderSide.SELL,
            Quantity(100000),
        )

        order1_filled = TestStubs.event_order_filled(
            order1,
            instrument=GBPUSD_FXCM,
            position_id=PositionId("P-1"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("1.00000"),
        )

        order2_filled = TestStubs.event_order_filled(
            order2,
            instrument=GBPUSD_FXCM,
            position_id=PositionId("P-2"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("1.00000"),
        )

        order3_filled = TestStubs.event_order_filled(
            order3,
            instrument=GBPUSD_FXCM,
            position_id=PositionId("P-3"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("1.00000"),
        )

        order4_filled = TestStubs.event_order_filled(
            order4,
            instrument=GBPUSD_FXCM,
            position_id=PositionId("P-3"),
            strategy_id=StrategyId("S", "1"),
            fill_price=Price("1.00100"),
        )

        position1 = Position(order1_filled)
        position2 = Position(order2_filled)
        position3 = Position(order3_filled)

        last_audusd = QuoteTick(
            AUDUSD_FXCM.symbol,
            Price("0.80501"),
            Price("0.80505"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        last_gbpusd = QuoteTick(
            GBPUSD_FXCM.symbol,
            Price("1.30315"),
            Price("1.30317"),
            Quantity(1),
            Quantity(1),
            UNIX_EPOCH,
        )

        self.data_cache.add_quote_tick(last_audusd)
        self.data_cache.add_quote_tick(last_gbpusd)
        self.portfolio.update_tick(last_audusd)
        self.portfolio.update_tick(last_gbpusd)

        # Act
        self.portfolio.update_position(TestStubs.event_position_opened(position1))
        self.portfolio.update_position(TestStubs.event_position_opened(position2))
        self.portfolio.update_position(TestStubs.event_position_opened(position3))

        position3.apply(order4_filled)
        self.portfolio.update_position(TestStubs.event_position_closed(position3))

        # Assert
        self.assertEqual(Money(-38998.00, USD), self.portfolio.unrealized_pnl_for_venue(FXCM))
        self.assertEqual(Money(161002.00, USD), self.portfolio.open_value(FXCM))
        self.assertEqual(Money(164.22, USD), self.portfolio.account(FXCM).position_margin())
        self.assertEqual(Money(0, BTC), self.portfolio.unrealized_pnl_for_venue(BINANCE))
        self.assertEqual(Money(0, BTC), self.portfolio.open_value(BINANCE))
        self.assertEqual(Decimal(200000), self.portfolio.net_position(AUDUSD_FXCM.symbol))
        self.assertEqual(Decimal(0), self.portfolio.net_position(GBPUSD_FXCM.symbol))
        self.assertTrue(self.portfolio.is_net_long(AUDUSD_FXCM.symbol))
        self.assertTrue(self.portfolio.is_flat(GBPUSD_FXCM.symbol))
        self.assertFalse(self.portfolio.is_completely_flat())