
def flatten_dict(d):
  flattened = []
  for k, v in d.items():
      if isinstance(v, list):
          for item in v:
              if isinstance(item, tuple):
                  flattened.extend(item)
              else:
                  flattened.append(item)
      else:
          flattened.append(v)
  return flattened



def extract_values(s):
  s = s.strip()
  lines = s.split('\n')
  values = []
  for line in lines:
      line = line.strip()
      if not line[0].isdigit() or line.startswith('!'):
          continue
      parts = line.split(',')
      x = float(parts[0].strip())
      y = float(parts[1].strip())
      values.append((x, y))
  return values


def extract_site_params(site_file_path ):

    # -- Extract site parameters :
    with open(site_file_path, 'r') as f:
        lines = f.readlines()

        site_parameters = []

        for line in lines:
            if not line.strip().startswith('*'):
                parts = line.split('=')
                if len(parts) == 2:
                    name = parts[0].strip()
                    value = float(parts[1].split('!')[0].strip())
                    site_parameters.append(value)
    return site_parameters

def extract_soil_params(soil_file_path):
  with open(soil_file_path, 'r') as f:
      lines = f.readlines()

  parsed_values = {}
  for i, line in enumerate(lines):
      if 'SMTAB' in line:
          key = 'SMTAB'
          value_str = line.strip() + ''.join(lines[i+1:i+10]).strip()
          parsed_values[key] = extract_values(value_str)
      elif 'CONTAB' in line:
          key = 'CONTAB'
          value_str = line.strip() + ''.join(lines[i+1:i+10]).strip()
          parsed_values[key] = extract_values(value_str)
      elif '**' in line or 'SOLNAM' in line :
          continue
      elif '=' in line:
          key, value_str = line.split('!')[0].split('=', 1)
          parsed_values[key.strip()] = float(value_str.strip())

  return flatten_dict(parsed_values)
