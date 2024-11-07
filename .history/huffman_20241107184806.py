import heapq
import os

class BinaryTree:
    def __init__(self, value, frequ):
        self.value = value
        self.frequ = frequ
        self.left = None
        self.right = None

    # Comparator for heap
    def __lt__(self, other):
        return self.frequ < other.frequ

class HuffmanCode:
    
    def __init__(self, path):
        self.path = path
        self.__heap = []
        self.__code = {}
        self.__reverse_code = {}
    
    def __frequency_from_text(self, text):
        frequ_dict = {}
        for char in text:
            if char not in frequ_dict:
                frequ_dict[char] = 0
            frequ_dict[char] += 1
        return frequ_dict

    def __build_heap(self, frequency_dict):
        for key in frequency_dict:
            frequency = frequency_dict[key]
            binary_tree_node = BinaryTree(key, frequency)
            heapq.heappush(self.__heap, binary_tree_node)

    def __build_binary_tree(self):
        while len(self.__heap) > 1:
            binary_tree_node_1 = heapq.heappop(self.__heap)
            binary_tree_node_2 = heapq.heappop(self.__heap)
            sum_of_freq = binary_tree_node_1.frequ + binary_tree_node_2.frequ
            new_node = BinaryTree(None, sum_of_freq)
            new_node.left = binary_tree_node_1
            new_node.right = binary_tree_node_2
            heapq.heappush(self.__heap, new_node)
        return

    def __build_tree_code_helper(self, root, curr_bits):
        if root is None:
            return
        if root.value is not None:
            self.__code[root.value] = curr_bits
            self.__reverse_code[curr_bits] = root.value
            return
        self.__build_tree_code_helper(root.left, curr_bits + '0')
        self.__build_tree_code_helper(root.right, curr_bits + '1')
        
    def __build_tree_code(self):
        root = heapq.heappop(self.__heap)
        self.__build_tree_code_helper(root, '')

    def __build_encoded_text(self, text):
        encoded_text = ''
        for char in text:
            encoded_text += self.__code[char]
        return encoded_text

    def __build_padded_text(self, encoded_text):
        padding_value = 8 - len(encoded_text) % 8
        for i in range(padding_value):
            encoded_text += '0'
        padding_info = "{0:08b}".format(padding_value)
        padded_text = padding_info + encoded_text
        return padded_text

    def __build_byte_array(self, padded_text):
        array = []
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i + 8]
            array.append(int(byte, 2))
        return array

    def compression(self):
        print("Compression starts")
        
        # Access the file and extract text from it
        filename, file_extension = os.path.splitext(self.path)
        output_path_file = filename + '.bin'
        
        with open(self.path, 'r+') as file, open(output_path_file, 'wb') as output:
            text = file.read()
            text = text.rstrip()
        
            # Calculate frequency of each character in the text
            frequency_dict = self.__frequency_from_text(text)
            
            # Build min heap from frequency dictionary
            self.__build_heap(frequency_dict)
            
            # Build binary tree from heap
            self.__build_binary_tree()
            
            # Build codes from binary tree and store them in the dictionary
            self.__build_tree_code()
            
            # Encode the text using the generated codes
            encoded_text = self.__build_encoded_text(text)
            
            # Pad the encoded text
            padded_text = self.__build_padded_text(encoded_text)
            
            # Convert padded text to a byte array
            byte_array = self.__build_byte_array(padded_text)
            final_bytes = bytes(byte_array)

            # Write the compressed data to the output file
            output.write(final_bytes)
        
        print('Compressed successfully')
        return output_path_file  # Return the path of the compressed file
    
    def __remove_padding(self, padded_text):
        # The first 8 bits are the padding information
        padding_info = padded_text[:8]
        padding_value = int(padding_info, 2)
        
        # Remove padding bits from the encoded text
        padded_text = padded_text[8:]
        encoded_text = padded_text[:-padding_value]
        return encoded_text

    def __decode_text(self, encoded_text):
        decoded_text = ""
        current_bits = ""
        for bit in encoded_text:
            current_bits += bit
            if current_bits in self.__reverse_code:
                character = self.__reverse_code[current_bits]
                decoded_text += character
                current_bits = ""
        return decoded_text

    def decompression(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed.txt"
        
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            # Read the binary file and convert it to a binary string
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            
            # Remove padding
            encoded_text = self.__remove_padding(bit_string)
            
            # Decode text
            decompressed_text = self.__decode_text(encoded_text)
            
            # Write decompressed text to output file
            output.write(decompressed_text)
        
        print("Decompression completed")
        return output_path

# Get the path from the user
path = input("Enter the path of the file: ")
h = HuffmanCode(path)
compressed_file_path = h.compression()
print(f"Compressed file saved at: {compressed_file_path}")

# To decompress, uncomment the line below
decompressed_file_path = h.decompression(compressed_file_path)
print(f"Decompressed file saved at: {decompressed_file_path}")
