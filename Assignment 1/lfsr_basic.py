class BasicLFSR:
    """
    Implements a basic Linear Feedback Shift Register (LFSR) with a hardwired feedback function.
    """
    def __init__(self, initial_state, feedback_taps):
        """
        Initializes the LFSR.

        Args:
            initial_state (str): Initial state of the LFSR (binary string).
            feedback_taps (list): List of tap positions (1-based index from the right).
        """
        self.state = list(initial_state)
        self.taps = sorted(feedback_taps, reverse=True)  # For easier indexing

    def get_current_state(self):
        """
        Retrieves the current state of the LFSR.

        Returns:
            str: The current state as a binary string.
        """
        return "".join(self.state)

    def generate_next_bit(self):
        """
        Generates the next stream bit and updates the state of the LFSR.

        Returns:
            int: The generated output bit (0 or 1).
        """
        output_bit = int(self.state[-1])

        # Calculate the feedback bit
        feedback_bit = 0
        for tap in self.taps:
            if tap <= len(self.state):
                feedback_bit ^= int(self.state[-tap])

        # Shift the state to the right and insert the feedback bit at the left
        self.state.insert(0, str(feedback_bit))
        self.state.pop()

        return output_bit

if __name__ == "__main__":
    initial_state = "0110"
    feedback_taps = [1, 4]  # Modified feedback taps
    num_iterations = 20

    lfsr_instance = BasicLFSR(initial_state, feedback_taps)

    print(f"Basic LFSR with initial state: {initial_state} and taps: {feedback_taps}")
    #print("----------------------------------------------------")
    #print("Step | State | Output Bit")
    print("--------------------------")
    print("| t  | R3 | R2 | R1 | R0 |")
    print("--------------------------")

    generated_output = []
    expected_output = []
    current_expected_state = initial_state

    for i in range(num_iterations):
        current_state = lfsr_instance.get_current_state()
        next_bit = lfsr_instance.generate_next_bit()
        generated_output.append((current_state, next_bit))
        #print(f"{i} | {current_state:4}  | {next_bit}")
        print(f"| {i:2} | {current_state[0]:2} | {current_state[1]:2} | {current_state[2]:2} | {current_state[3]:2} |")

        # Manually calculate the expected output for verification with taps [1, 4]
        output_bit_expected = int(current_expected_state[-1])
        feedback_bit_expected = 0
        for tap in feedback_taps:
            if tap <= len(current_expected_state):
                feedback_bit_expected ^= int(current_expected_state[-tap])
        next_expected_state = str(feedback_bit_expected) + current_expected_state[:-1]
        expected_output.append((current_expected_state, output_bit_expected))
        current_expected_state = next_expected_state

    print("\nVerification:")
    if generated_output == expected_output:
        print("Generated output matches the expected output.")
    else:
        print("Generated output does NOT match the expected output.")
        print("Generated:", generated_output)
        print("Expected:", expected_output)
