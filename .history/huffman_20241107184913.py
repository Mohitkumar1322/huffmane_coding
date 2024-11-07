# huffman_code.py

import heapq
import os
import concurrent.futures

class BinaryTree:
    def __init__(self, value, frequ):
        self.value = value
        self.frequ = frequ
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequ < other.frequ

class HuffmanCode:
    
    def __init__(self, path):
        self.path = path
        self.__heap = []
        self.__code = {}
    
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
            node1 = heapq.heappop(self.__heap)
            node2 = heapq.heappop(self.__heap)
            sum_freq = node1.frequ + node2.frequ
            new_node = BinaryTree(None, sum_freq)
            new_node.left = node1
            new_node.right = node2
            heapq.heappush(self.__heap, new_node)
    
    def __build_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.value is not None:
            self.__code[root.value] = current_code
            return
        self.__build_codes_helper(root.left, current_code + '0')
        self.__build_codes_helper(root.right, current_code + '1')
        
    def __build_codes(self):
        root = heapq.heappop(self.__heap)
        self.__build_codes_helper(root, '')

    def __encode_text_parallel(self, text):
        chunk_size = 10000
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            encoded_chunks = list(executor.map(self.__encode_chunk, chunks))
        
        return ''.join(encoded_chunks)
    
    def __encode_chunk(self, chunk):
        return ''.join(self.__code[char] for char in chunk)

    def __pad_encoded_text(self, encoded_text):
        padding_value = 8 - len(encoded_text) % 8
        encoded_text += '0' * padding_value
        padding_info = "{0:08b}".format(padding_value)
        return padding_info + encoded_text

    def __byte_array(self, padded_text):
        return [int(padded_text[i:i + 8], 2) for i in range(0, len(padded_text), 8)]

    def compression(self):
        filename, _ = os.path.splitext(self.path)
        output_path = filename + '.bin'
        
        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read().rstrip()
            frequency_dict = self.__frequency_from_text(text)
            
            self.__build_heap(frequency_dict)
            self.__build_binary_tree()
            self.__build_codes()
            
            encoded_text = self.__encode_text_parallel(text)
            padded_text = self.__pad_encoded_text(encoded_text)
            byte_array = self.__byte_array(padded_text)
            output.write(bytes(byte_array))
        
        return output_path
