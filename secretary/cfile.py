class CFile(object):
    def __init__(self, path):
        self._path = path
        
        self._code = []
        
        with open(self._path, 'r') as file:
            for line in file:
                self._code.append(line.rstrip())

    @property
    def path(self):
        return self._path

    @property
    def code(self):
        return self._code

    @property
    def functions(self):
        return self._get_functions()

    def __repr__(self):
        s = self._path + " (" + str(len(self.code)) + " LOC):\n"
        s += "\tContaining " + str(len(self.functions))
        s += " function definition"

        # the lengths we go to for correct grammar
        if len(self.functions) > 1:
            s += "s"
        
        s += ":\n"

        for f in self.functions:
            s += "\t\t" + f["type"] + " " + f["name"] + "("

            for i in range(len(f["parameters"])):
                s += f["parameters"][i]
                if i < len(f["parameters"]) - 1:
                    s += ", "

            s += ")\n"

        return s

    def _contains_type(self, string):
        types = ["unsigned", "signed", "char", "int", "short", "long", "double",
                 "float", "const"]
        
        for t in types:
            if t in string:
                t_loc = string.find(t)
                
                if t_loc > 0 or t_loc + len(t) < len(string):
                    if string[t_loc-1].isspace() and \
                       string[t_loc+len(t)].isspace():
                        return True
                else:
                    return True
            
        return False

    def _parse_function_definition(self, string):
        # params
        params_start = string.find("(")
        params_end = string.find(")")
        params_list = string[params_start+1:params_end].split(",")

        params = []

        for p in params_list:
            params.append(p.strip())
        
        split_list = string[:params_start].split(" ")

        name = ""
        return_type_elems = []

        for i in range(len(split_list)):
            if self._contains_type(split_list[i]):
                if i < len(split_list) - 1:
                    return_type_elems.append(split_list[i])
            else:
                name = split_list[i]

        return_type = ""

        for elem in return_type_elems:
            return_type += elem + " "

        defn = {"type": return_type.rstrip(),
                "name": name,
                "parameters": params}

        return defn

    def _get_functions(self):
        functions = []
        
        for line in self.code:
            if "=" not in line and "->" not in line:
                if self._contains_type(line) and "(" in line and ")" in line:
                    functions.append(self._parse_function_definition(line))

        return functions
