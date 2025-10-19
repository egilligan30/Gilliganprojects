from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'demo_app'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 25
    MORTGAGE_PAYMENT = cu(25)
    DEBT_LIMIT = cu(500)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bet_amount = models.CurrencyField(
        label="Enter your bet amount:",
        min=cu(0),
        max=cu(250),
        initial=cu(0)
    )
    bet_odds = models.FloatField(label="Choose your bet odds", min=-400, max=400)
    bet_outcome = models.CurrencyField(initial=cu(0))
    savings = models.CurrencyField(initial=cu(250))
    debt = models.CurrencyField(initial=cu(0))
    mortgage_paid = models.BooleanField(initial=False)
    bankrupt = models.BooleanField(initial=False)

def process_bet(player: Player):
    # Carry over from previous round
    if player.round_number > 1:
        prev = player.in_round(player.round_number - 1)
        player.savings = prev.savings
        player.debt = prev.debt

    bet = player.bet_amount or cu(0)
    odds = player.bet_odds or 0

    if odds < 0:
        multiplier = 100 / abs(odds)
    else:
        multiplier = odds / 100

    win_prob = max(0.05, min(0.95, 0.5 + (-odds / 800)))

    if random.random() < win_prob:
        player.bet_outcome = cu(bet * multiplier)
        player.savings += bet + player.bet_outcome
    else:
        player.bet_outcome = -bet
        player.savings -= bet

    if player.savings >= C.MORTGAGE_PAYMENT:
        player.savings -= C.MORTGAGE_PAYMENT
        player.mortgage_paid = True
    else:
        unpaid = C.MORTGAGE_PAYMENT - player.savings
        player.debt += unpaid
        player.savings = cu(0)
        player.mortgage_paid = False

    player.bankrupt = player.debt >= C.DEBT_LIMIT

class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Bet(Page):
    form_model = 'player'
    form_fields = ['bet_amount', 'bet_odds']

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= 5:
            min_odds, max_odds = -200, 200
        else:
            min_odds, max_odds = -400, 400

        if player.round_number > 1:
            prev = player.in_round(player.round_number - 1)
            current_savings = prev.savings
            current_debt = prev.debt
            current_odds = prev.bet_odds
        else:
            current_savings = player.savings
            current_debt = player.debt
            current_odds = 0  # default to 0

        return dict(
            ROUND_NUMBER=player.round_number,
            NUM_ROUNDS=C.NUM_ROUNDS,
            SAVINGS=current_savings,
            DEBT=current_debt,
            MIN_ODDS=min_odds,
            MAX_ODDS=max_odds,
            CURRENT_ODDS=current_odds,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        process_bet(player)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            ROUND_NUMBER=player.round_number,
            NUM_ROUNDS=C.NUM_ROUNDS,
            SAVINGS=player.savings,
            DEBT=player.debt,
            BET_OUTCOME=player.bet_outcome,
            BET_CHOICE=player.bet_odds,
            BET_AMOUNT=player.bet_amount,
            MORTGAGE_PAID=player.mortgage_paid,
            BANKRUPT=player.bankrupt,
            ALL_ROUNDS=player.in_all_rounds()
        )


page_sequence = [Introduction, Instructions, Bet, Results]
