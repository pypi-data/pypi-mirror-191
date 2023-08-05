# binarysearch_build

A simple implementation of binary search in Python.

# Binary Search

Binary Search is a searching algorithm used in a sorted array by repeatedly dividing the search interval in half.

## Installation

- Make sure you have Python installed in your system.
- Run Following command in the CMD.

 ```
  pip install search_binary
  ```

  
## Usage

Here's an example of how to use the `binary_search` function:

```
from search_binary import binary_search

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
target = 5
result = binary_search(arr, target)
print(result) # Output: 4
```

The `binary_search` function takes in two arguments: `arr` and `target`. The `arr` argument is a list of sorted values, and the `target` argument is the value you're searching for in the list. The function returns the index of the target value in the list, or `-1` if the target value is not found.

## Contributing

Contributions are welcome! If you'd like to contribute, simply fork the repository, make your changes, and submit a pull request.

## License

This package is licensed under the MIT License. See the `LICENSE` file for details.



