# import os
# import pickle
# import math
#
# __author__ = "John Conwell"
# __copyright__ = "John Conwell"
# __license__ = "MIT"

# # from fqdn_parser.char_probabilities import download_umbrella_feed, calc_char_probabilities, get_reg_domain, clean_fqdn
#
# from fqdn_parser.suffixes import Suffixes, ParsedResult
#
#
#
# class Entropy:
#     UMBRELLA_FEED_PATH = "umbrella_feed.txt"
#
#     def __init__(self, top_n_fqdns=999999999, read_cache=True, save_cache=True,
#                  cache_path="entropy.cache", verbose=False, domain_suffixes=None):
#         if read_cache and cache_path and os.path.exists(cache_path):
#             with open(cache_path, 'rb') as handle:
#                 domain_char_probs, fqdn_char_probs = pickle.load(handle)
#         else:
#             download_umbrella_feed(Entropy.UMBRELLA_FEED_PATH)
#             domain_char_probs, fqdn_char_probs = calc_char_probabilities(
#                 Entropy.UMBRELLA_FEED_PATH, top_n_fqdns, verbose)
#             os.remove(Entropy.UMBRELLA_FEED_PATH) if os.path.exists(Entropy.UMBRELLA_FEED_PATH) else None
#             if save_cache and cache_path:
#                 with open(cache_path, 'wb') as handle:
#                     pickle.dump((domain_char_probs, fqdn_char_probs), handle)
#         self._domain_char_probs = domain_char_probs
#         self._fqdn_char_probs = fqdn_char_probs
#         if domain_suffixes is None:
#             domain_suffixes = Suffixes()
#         self._suffixes = domain_suffixes
#
#     @staticmethod
#     def relative_entropy(data, probabilities, base=2):
#         '''
#         Calculate the relative entropy (Kullback-Leibler divergence) between data and expected values
#         '''
#         from collections import Counter
#         entropy = 0.0
#         length = len(data) * 1.0
#         if length > 0:
#             cnt = Counter(data)
#             for char, count in cnt.items():
#                 observed = count / length
#                 expected = probabilities[char]
#                 entropy += observed * math.log((observed / expected), base)
#         return entropy
#
#     def domain_entropy(self, parsed_result: ParsedResult, base: int = 2):
#         self.domain_entropy(parsed_result.registrable_domain_host, base)
#
#     def domain_entropy(self, domain_name: str, base: int = 2):
#         domain_name = get_reg_domain(self._suffixes, domain_name)
#         if domain_name:
#             return self.relative_entropy(domain_name, self._domain_char_probs, base)
#         return 0
#
#     def fqdn_entropy(self, fqdn, base=2):
#         fqdn = clean_fqdn(self._suffixes, fqdn)
#         if fqdn:
#             return self.relative_entropy(fqdn, self._fqdn_char_probs, base)
#         return 0
#
#
# def main():
#     entropy = Entropy()
#     # legit'ish looking entropy example
#     fqdn = "microsoft.com"
#     entropy_score = entropy.domain_entropy(fqdn)
#     print(entropy_score)
#
#     suffixes = Suffixes(read_cache=False)
#     result = suffixes.parse(fqdn)
#     entropy_score = entropy.domain_entropy(result)
#     print(entropy_score)
#
#     # entropy_score = entropy.fqdn_entropy("stuff.things.microsoft.com")
#     # print(entropy_score)
#     # # keyboard smash entropy example
#     # entropy_score = entropy.domain_entropy("lk3k3l24jlk23.com")
#     # print(entropy_score)
#     # entropy_score = entropy.fqdn_entropy("lkdjcf.pqxikf.lk3k3l24jlk23.com")
#     # print(entropy_score)
#
#
# if __name__ == "__main__":
#     main()
