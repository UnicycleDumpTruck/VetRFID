import mercury


# class izarReader():
#     def __init__(self):
#         self.reader = mercury.Reader(
#             "llrp://izar-51e4c8.local", protocol="GEN2")
#         print(self.reader.get_model())
#         self.reader.set_read_plan([1, 2], "GEN2", read_power=1500)
#         return self.reader


class izarReader(mercury.Reader):
    def __init__(self, *args, **kwargs):
        super().__init__(uri='llrp://izar-51e4c8.local', protocol="GEN2", *args, **kwargs)
        print(self.reader.get_model())
        self.reader.set_read_plan([1, 2], "GEN2", read_power=1500)
        # return self ?
