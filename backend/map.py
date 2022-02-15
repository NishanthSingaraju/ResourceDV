import ee
import pandas as pd

ee.Initialize()


def get_bounds():
  stateFilter = ee.Filter.equals("STUSPS", "NC")
  NC = ee.FeatureCollection('TIGER/2016/States').filter(stateFilter)
  return NC


def get_map():
  NC = get_bounds()
  dataset = ee.FeatureCollection('TIGER/2016/Counties').filterBounds(NC)
  visParams = {
      "palette": ['yellow', 'blue', 'green', 'purple', 'pink', 'red'],
      "min": 0,
      "max": 50,
      "opacity": 0.8,
  }

  stateDataset = ee.FeatureCollection('TIGER/2016/States').filterBounds(NC)
  dataset = ee.FeatureCollection(
      dataset.map(
          lambda f: f.set('STATEFP', ee.Number.parse(f.get('STATEFP')))))

  image = ee.Image().float().paint(dataset, 'STATEFP').clip(NC)
  countyOutlines = ee.Image().float().paint(dataset, 'black', 1).clip(NC)
  stateOutlines = ee.Image().float().paint(stateDataset, 'black', 3).clip(NC)

  return image.getMapId(
      visParams)['tile_fetcher'].url_format, countyOutlines.getMapId(
          visParams)['tile_fetcher'].url_format, stateOutlines.getMapId(
              visParams)['tile_fetcher'].url_format

def convert_csv_to_json():
    df = pd.read_csv('/Users/nishanthsingaraju/nccadv/backend/resource.csv')
    def create_position(row):
        try:
            lat, lon = row["Coordinates"].split(",")
            if float(lat) > 36.576:
                return []
            return [float(lat), float(lon)]
        except:
            return []

    df.rename({'Type: Shelter, Food, Medical, LGBT, Mental health': 'Type'}, axis=1, inplace=True)
    print(df)
    df["positions"] = df.apply(create_position, axis = 1)
    df = df[df["positions"].map(lambda d: len(d)) > 0]
    print(df)
    df.to_json('resource.json', orient='records')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  convert_csv_to_json()
