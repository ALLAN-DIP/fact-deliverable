"""Bots that carry out random orders and make random order proposals."""

from abc import ABC
from dataclasses import dataclass
import random
from typing import Dict, List, Optional, Sequence

from daidepp import AND, PRP, XDO
from diplomacy.utils import strings as diplomacy_strings
from diplomacy.utils.constants import SuggestionType

from chiron_utils.bots.baseline_bot import BaselineBot, BotType
from chiron_utils.daide2eng import gen_english
from chiron_utils.parsing_utils import dipnet_to_daide_parsing
from chiron_utils.utils import get_other_powers


@dataclass
class RandomProposerBot(BaselineBot, ABC):
    """Bot that carries out random orders and sends random order proposals to other bots.

    Because of the similarity between the advisor and player versions of this bot,
    both of their behaviors are abstracted into this single abstract base class.
    """

    is_first_messaging_round = False

    async def start_phase(self) -> None:
        """Execute actions at the start of the phase."""
        self.is_first_messaging_round = True

    def get_random_proposal_orders(self) -> Dict[str, str]:
        """Generate random order proposals for other powers.

        Returns:
            Mapping from powers to random order proposals.
        """
        proposals = {}

        # For each power, randomly sample a valid order
        for other_power in get_other_powers([self.power_name], self.game):
            suggested_random_orders = self.get_random_orders(other_power)
            suggested_random_orders = list(
                filter(
                    lambda x: x != diplomacy_strings.WAIVE
                    and not x.endswith(diplomacy_strings.VIA),
                    suggested_random_orders,
                )
            )
            if len(suggested_random_orders) > 0:
                commands = dipnet_to_daide_parsing(suggested_random_orders, self.game)
                random_orders = [XDO(command) for command in commands]
                if len(random_orders) > 1:
                    suggested_random_orders = PRP(AND(*random_orders))
                else:
                    suggested_random_orders = PRP(*random_orders)

                proposals[other_power] = gen_english(suggested_random_orders)

        return proposals

    async def do_messaging_round(self, orders: Sequence[str]) -> List[str]:
        """Carry out one round of messaging, along with related tasks.

        Returns:
            List of orders to carry out.
        """
        if not self.is_first_messaging_round:
            return list(orders)

        random_order_proposals = self.get_random_proposal_orders()

        for other_power, suggested_random_orders in random_order_proposals.items():
            if self.bot_type == BotType.ADVISOR:
                await self.suggest_message(other_power, suggested_random_orders)
                await self.suggest_commentary(other_power, f"I have advice about {other_power}!")
            elif self.bot_type == BotType.PLAYER:
                await self.send_message(other_power, suggested_random_orders)

        self.is_first_messaging_round = False

        return list(orders)

    def get_random_orders(self, power_name: Optional[str] = None) -> List[str]:
        """Generate random orders for a power to carry out.

        Args:
            power_name: Name of power to generate random orders for.
                Defaults to current power.

        Returns:
            List of random orders.
        """
        if power_name is None:
            power_name = self.power_name

        possible_orders = self.game.get_all_possible_orders()
        orders = [
            random.choice(list(possible_orders[loc]))
            for loc in self.game.get_orderable_locations(power_name)
            if possible_orders[loc]
        ]
        return orders

    async def gen_orders(self) -> List[str]:
        """Generate orders for a turn.

        Returns:
            List of orders to carry out.
        """
        orders = self.get_random_orders()
        if self.bot_type == BotType.ADVISOR:
            await self.suggest_orders(orders)

            random_predicted_orders = {}
            for other_power in get_other_powers([self.power_name], self.game):
                random_predicted_orders[other_power] = self.get_random_orders(other_power)
            await self.suggest_opponent_orders(random_predicted_orders)
        elif self.bot_type == BotType.PLAYER:
            await self.send_orders(orders, wait=True)
        return orders


@dataclass
class RandomProposerAdvisor(RandomProposerBot):
    """Advisor form of `RandomProposerBot`."""

    bot_type = BotType.ADVISOR
    default_suggestion_type = (
        SuggestionType.MESSAGE
        | SuggestionType.MOVE
        | SuggestionType.COMMENTARY
        | SuggestionType.OPPONENT_MOVE
    )


@dataclass
class RandomProposerPlayer(RandomProposerBot):
    """Player form of `RandomProposerBot`."""

    bot_type = BotType.PLAYER
