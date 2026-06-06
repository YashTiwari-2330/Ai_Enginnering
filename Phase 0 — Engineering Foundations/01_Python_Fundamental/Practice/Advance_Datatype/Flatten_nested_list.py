def flatten_patten(nums):
    result = []

    for item in nums:
        if isinstance(item , list):
            result.extend(flatten_patten(item))

        else:
            result.append(item)

    return result

nums = [1,2,[3,[4,5]]]
print(flatten_patten(nums))