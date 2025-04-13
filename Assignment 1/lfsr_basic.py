class BasicLFSR:
    
    # Implementasi basic Linear Feedback Shift Register (LFSR) dengan hardwired feedback function.
    
    def __init__(self, initial_state, feedback_taps):
        
        # initial_state (str): initial state
        # feedback_taps (list): list posisi tap (index basis-1 dari kanan) 
        self.state = list(initial_state)
        self.taps = sorted(feedback_taps, reverse=True)  # For easier indexing

    def get_current_state(self):
        return "".join(self.state)

    def generate_next_bit(self):
        output_bit = int(self.state[-1])

        # Menghitung bit feedback
        feedback_bit = 0
        for tap in self.taps:
            if tap <= len(self.state):
                feedback_bit ^= int(self.state[-tap])

        # memindah state ke kanan dan memasukkan feedback bit ke kiri
        self.state.insert(0, str(feedback_bit))
        self.state.pop()

        return output_bit

if __name__ == "__main__":
    initial_state = "0110"
    feedback_taps = [1, 4]
    num_iterations = 20

    lfsr_instance = BasicLFSR(initial_state, feedback_taps)

    print(f"Basic LFSR dengan initial state: {initial_state} dan taps: {feedback_taps}")
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
        print("Generated output matches expected output.")
    else:
        print("Generated output does NOT match expected output.")
        print("Generated:", generated_output)
        print("Expected:", expected_output)
