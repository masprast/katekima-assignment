
class GeneralLFSR:
    """
    Implements a general Linear Feedback Shift Register (LFSR).
    """
    def __init__(self, size, taps, initial_state=None):
        """
        Initializes the General LFSR.

        Args:
            size (int): The size (number of bits) of the register.
            taps (list): List of tap positions (1-based index from the right) for feedback.
            initial_state (str, optional): Initial state of the register (binary string).
                                          If None, the register is initialized to all zeros.
        """
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Register size must be a positive integer.")
        if not isinstance(taps, list) or not all(isinstance(tap, int) and 1 <= tap <= size for tap in taps):
            raise ValueError("Taps must be a list of integers between 1 and register size.")
        if initial_state is not None:
            if not isinstance(initial_state, str) or len(initial_state) != size or not all(bit in '01' for bit in initial_state):
                raise ValueError(f"Initial state must be a binary string of length {size}.")
            self.state = list(initial_state)
        else:
            self.state = ['0'] * size
        self.size = size
        self.taps = sorted(taps, reverse=True)

    def get_register_size(self):
        """
        Returns the size of the LFSR register.
        """
        return self.size

    def set_register_size(self, size):
        """
        Sets the size of the LFSR register. Resets the state to zeros.

        Args:
            size (int): The new size of the register.
        """
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Register size must be a positive integer.")
        self.size = size
        self.state = ['0'] * size
        self.taps = [tap for tap in self.taps if tap <= size]
        self.taps.sort(reverse=True)

    def get_current_state(self):
        """
        Returns the current state of the LFSR as a binary string.
        """
        return "".join(self.state)

    def set_current_state(self, new_state):
        """
        Sets the current state of the LFSR.

        Args:
            new_state (str): The new state as a binary string.
        """
        if not isinstance(new_state, str) or len(new_state) != self.size or not all(bit in '01' for bit in new_state):
            raise ValueError(f"New state must be a binary string of length {self.size}.")
        self.state = list(new_state)

    def get_tap_sequence(self):
        """
        Returns the list of tap indices.
        """
        return sorted(self.taps)

    def set_tap_sequence(self, taps):
        """
        Sets the tap sequence for the LFSR.

        Args:
            taps (list): A list of tap positions (1-based index from the right).
        """
        if not isinstance(taps, list) or not all(isinstance(tap, int) and 1 <= tap <= self.size for tap in taps):
            raise ValueError(f"Taps must be a list of integers between 1 and {self.size}.")
        self.taps = sorted(list(set(taps)), reverse=True) # Ensure unique and sorted

    def reset(self, initial_state=None):
        """
        Resets the LFSR register.

        Args:
            initial_state (str, optional): The state to reset to. If None, resets to all zeros.
        """
        if initial_state is not None:
            self.set_current_state(initial_state)
        else:
            self.state = ['0'] * self.size

    def next_bit(self):
        """
        Generates the next stream bit and updates the state of the LFSR.

        Returns:
            int: The generated output bit (0 or 1).
        """
        output_bit = int(self.state[-1])

        # Calculate the feedback bit
        feedback_bit = 0
        for tap in self.taps:
            if tap <= self.size:
                feedback_bit ^= int(self.state[-tap])

        # Shift the state to the right and insert the feedback bit at the left
        self.state.insert(0, str(feedback_bit))
        self.state.pop()

        return output_bit

if __name__ == "__main__":
    # 1. Instantiate GeneralLFSR to match the basic LFSR
    initial_state_basic = "0110"
    feedback_taps_basic = [1, 4]
    register_size_basic = len(initial_state_basic)

    general_lfsr_instance = GeneralLFSR(register_size_basic, feedback_taps_basic, initial_state_basic)

    print("General LFSR Configuration:")
    print(f"  Register Size: {general_lfsr_instance.get_register_size()}")
    print(f"  Initial State: {general_lfsr_instance.get_current_state()}")
    print(f"  Tap Sequence: {general_lfsr_instance.get_tap_sequence()}")
    print("----------------------------------------------------")
    print("Step | State | Output Bit (General LFSR)")
    print("----------------------------------------------------")

    generated_output_general = []
    for i in range(20):
        current_state = general_lfsr_instance.get_current_state()
        next_bit = general_lfsr_instance.next_bit()
        generated_output_general.append((current_state, next_bit))
        print(f"{i+1:4} | {current_state:4}  | {next_bit}")

    print("\n--- Verifying against Basic LFSR ---")

    class BasicLFSR:
        """Implements a basic Linear Feedback Shift Register (LFSR)."""
        def __init__(self, initial_state, feedback_taps):
            self.state = list(initial_state)
            self.taps = sorted(feedback_taps, reverse=True)
        def get_current_state(self):
            return "".join(self.state)
        def generate_next_bit(self):
            output_bit = int(self.state[-1])
            feedback_bit = 0
            for tap in self.taps:
                if tap <= len(self.state):
                    feedback_bit ^= int(self.state[-tap])
            self.state.insert(0, str(feedback_bit))
            self.state.pop()
            return output_bit

    basic_lfsr_instance = BasicLFSR(initial_state_basic, feedback_taps_basic)

    print("----------------------------------------------------")
    print("Step | State | Output Bit (Basic LFSR)")
    print("----------------------------------------------------")

    generated_output_basic = []
    for i in range(20):
        current_state = basic_lfsr_instance.get_current_state()
        next_bit = basic_lfsr_instance.generate_next_bit()
        generated_output_basic.append((current_state, next_bit))
        print(f"{i+1:4} | {current_state:4}  | {next_bit}")

    # 2. Verify it produces the same output
    if generated_output_general == generated_output_basic:
        print("\nVerification: General LFSR output matches Basic LFSR output.")
    else:
        print("\nVerification: General LFSR output DOES NOT match Basic LFSR output.")
        print("General LFSR Output:", generated_output_general)
        print("Basic LFSR Output:", generated_output_basic)
