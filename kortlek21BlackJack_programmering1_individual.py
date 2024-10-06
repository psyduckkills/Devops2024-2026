#Inlämmning för Programmering 1 
# 6okt 2024


import random

# Game rules text
rule_txt = str("""-------Here is how you play black jack! ------------
 \nThis game is about playing against the house (the casino). 
 The dealer and you play with a deck of cards.
 Each card has a value between 1-11.
 All royal cards except Ace has a value of 10.
 Ace has a value of either 1 or 11, you can choose.
 You first see your hand of two cards.
 The dealer only reveals their first card.
 You then decide if you want to keep your cards or hit (get another card).
 If you want another card, the dealer's other card is revealed.
 If your total value is above 21, the house (dealer) wins.
 If you have a higher value in your hand than the dealer, it means you win.
\n You must be over 18 years old.""")
 
# Deck with cards and values (simplified without suits)
card_deck = [("A", 11), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7), ("8", 8), ("9", 9), ("10", 10), ("J", 10), ("Q", 10), ("K", 10)] * 4

# Shuffle the deck
random.shuffle(card_deck)

# Starting funds
player_funds = 100

# Dealer's and player's hands
player_hand = []
dealer_hand = []

# Function to deal a card
def deal_card(hand):
    card = card_deck.pop()  # Remove a card from the deck
    hand.append(card)  # Add it to the hand (dealer or player)

# Function to calculate total value, considering the Ace (1 or 11)
def calculate_total(hand):
    total = 0
    ace_count = 0
    for card, value in hand:
        total += value
        if card == "A":
            ace_count += 1
    # Adjust Aces from 11 to 1 if needed
    while ace_count > 0 and total > 21:
        total -= 10
        ace_count -= 1
    return total

# Function to display dealer's hand, hiding the second card initially
def reveal_dealer_hand(hidden=True):
    if hidden:
        return f"{dealer_hand[0][0]} and [Hidden]"
    else:
        return ', '.join([f"{card[0]}" for card in dealer_hand])

# Function to display player's hand
def reveal_player_hand():
    return ', '.join([f"{card[0]}" for card in player_hand])

# Main Blackjack game logic
def play_blackjack(user_player, starting_sum):
    balance = starting_sum
    print(f"\nWelcome {user_player}! You have a starting balance of ${balance}.")
    
    global player_hand, dealer_hand

    while balance > 0:
        print(f"\nCurrent balance: ${balance}")
        # Get player's bet
        while True:
            try:
                bet = int(input("Place your bet: $"))
                if 0 < bet <= balance:
                    break
                else:
                    print(f"Invalid bet. You must bet between $1 and ${balance}.")
            except ValueError:
                print("Please enter a valid amount.")
        
        # Reset deck, hands, and shuffle again for each round
        card_deck = [("A", 11), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7), ("8", 8), ("9", 9), ("10", 10), ("J", 10), ("Q", 10), ("K", 10)] * 4
        random.shuffle(card_deck)
        player_hand = []
        dealer_hand = []
        
        # Initial deal of two cards each
        for _ in range(2):
            deal_card(player_hand)
            deal_card(dealer_hand)
        
        # Player's turn
        while True:
            print(f"\nDealer has: {reveal_dealer_hand(hidden=True)}")
            print(f"You have: {reveal_player_hand()} (Total: {calculate_total(player_hand)})")
            
            if calculate_total(player_hand) == 21:
                print("Blackjack! You win!")
                balance += bet  # Player wins the bet
                break
            
            if calculate_total(player_hand) > 21:
                print(f"You have busted with a total of {calculate_total(player_hand)}! Dealer wins.")
                balance -= bet  # Player loses the bet
                break

            choice = input("Do you want to (h) Hit or (s) Stand? ").lower()
            if choice == "h":
                deal_card(player_hand)
            elif choice == "s":
                break
            else:
                print("Invalid choice, please try again.")
        
        # Dealer's turn (only if the player hasn't busted)
        if calculate_total(player_hand) <= 21:
            while calculate_total(dealer_hand) < 17:
                deal_card(dealer_hand)
        
            # Final hands revealed
            print(f"\nDealer's hand: {reveal_dealer_hand(hidden=False)} (Total: {calculate_total(dealer_hand)})")
            print(f"Your hand: {reveal_player_hand()} (Total: {calculate_total(player_hand)})")

            # Determine the winner
            player_total = calculate_total(player_hand)
            dealer_total = calculate_total(dealer_hand)

            if dealer_total > 21:
                print(f"Dealer busted with a total of {dealer_total}. You win!")
                balance += bet
            elif player_total > dealer_total:
                print(f"You win with a total of {player_total}!")
                balance += bet
            elif dealer_total > player_total:
                print(f"Dealer wins with a total of {dealer_total}.")
                balance -= bet
            else:
                print("It's a tie!")
        
        # Ask to play again or cash out
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            print(f"Thanks for playing, {user_player}! You leave with ${balance}.")
            break

# Main menu system
def main_menu():
    print("------- Blackjack Menu ----------")
    print("1. Play Blackjack")
    print("2. Refill Cash")
    print("3. Cash Out and Exit")
    choice = input("Enter the choice (1-3): ")

    while choice not in ["1", "2", "3"]:
        print("Invalid option. Please try again.")
        choice = input("Enter the choice (1-3): ")

    return choice

# Cash refill function
def refill_cash():
    global player_funds
    refill_amount = int(input("Enter the amount you want to add: "))
    player_funds += refill_amount
    print(f"Your total funds have been updated to ${player_funds:.2f}")

# Age verification function
def verify_age():
    print("-------------Welcome to BlackJack---------------------")
    print(rule_txt)
    print()  # Create space
    

    age = input("Enter your age: ")
    print()  # Create space

    while not age.isdigit() or int(age) < 18:
        if not age.isdigit():
            print("Invalid input. Please enter a valid number for your age.")
        elif int(age) < 18:
            print("You must be 18 or older to play Blackjack.")
            exit()
        age = input("Enter your age: ")

    print("Welcome to the Blackjack game!")

# Main program
def blackjack_game():
    # Age verification
    verify_age()

    while True:
        # Display the menu and get user choice
        choice = main_menu()

        if choice == "1":
            play_blackjack("Player", player_funds)
        elif choice == "2":
            refill_cash()
        elif choice == "3":
            print(f"Thanks for playing! You leave with ${player_funds}.")
            break

# Start the game
blackjack_game()
