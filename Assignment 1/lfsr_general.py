
class GeneralLFSR:
    
    # Implementasi general Linear Feedback Shift Register (LFSR).
    
    def __init__(self, size, taps, initial_state=None):
        # size (int): jumblah bit register
        # taps: (list): list posisi tap (index basis-1 dari kanan)
        # initial_state (str): initial state
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Register size harus integer positif.")
        if not isinstance(taps, list) or not all(isinstance(tap, int) and 1 <= tap <= size for tap in taps):
            raise ValueError("Taps harus berupa list integers antara 1-size register.")
        if initial_state is not None:
            if not isinstance(initial_state, str) or len(initial_state) != size or not all(bit in '01' for bit in initial_state):
                raise ValueError(f"Initial state harus berupa string binary {size}.")
            self.state = list(initial_state)
        else:
            self.state = ['0'] * size
        self.size = size
        self.taps = sorted(taps, reverse=True)

    def get_register_size(self):
        return self.size

    def set_register_size(self, size):
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Register size must be a positive integer.")
        self.size = size
        self.state = ['0'] * size
        self.taps = [tap for tap in self.taps if tap <= size]
        self.taps.sort(reverse=True)

    def get_current_state(self):
        return "".join(self.state)

    def set_current_state(self, new_state):
        if not isinstance(new_state, str) or len(new_state) != self.size or not all(bit in '01' for bit in new_state):
            raise ValueError(f"New state must be a binary string of length {self.size}.")
        self.state = list(new_state)

    def get_tap_sequence(self):
        return sorted(self.taps)

    def set_tap_sequence(self, taps):
        if not isinstance(taps, list) or not all(isinstance(tap, int) and 1 <= tap <= self.size for tap in taps):
            raise ValueError(f"Taps must be a list of integers between 1 and {self.size}.")
        self.taps = sorted(list(set(taps)), reverse=True) # Ensure unique and sorted

    def reset(self, initial_state=None):
        if initial_state is not None:
            self.set_current_state(initial_state)
        else:
            self.state = ['0'] * self.size

    def next_bit(self):
        output_bit = int(self.state[-1])

        # menghitung feedback bit
        feedback_bit = 0
        for tap in self.taps:
            if tap <= self.size:
                feedback_bit ^= int(self.state[-tap])

        # memindah state ke kanan dan memasukkan feedback bit ke kiri
        self.state.insert(0, str(feedback_bit))
        self.state.pop()

        return output_bit

if __name__ == "__main__":
    # 1. Instantiate GeneralLFSR agar match dengan basic LFSR
    initial_state_basic = "0110"
    feedback_taps_basic = [1, 4]
    register_size_basic = len(initial_state_basic)

    general_lfsr_instance = GeneralLFSR(register_size_basic, feedback_taps_basic, initial_state_basic)

    print("Konfigurasi General LFSR:")
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

    # 2. Verify the same output
    if generated_output_general == generated_output_basic:
        print("\nVerification: General LFSR output matches Basic LFSR output.")
    else:
        print("\nVerification: General LFSR output DOES NOT match Basic LFSR output.")
        print("General LFSR Output:", generated_output_general)
        print("Basic LFSR Output:", generated_output_basic)
