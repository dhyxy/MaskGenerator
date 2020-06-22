import json
from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw


class MaskGenerator:
    """This will work for any format through the VGG Image annotator as long as there
    is only one "Type" in the attributes.
    """

    def __init__(self, json_file: str, img_dir: str, out_dir: str):
        """Generate black and white masks through json file with annotation data.

        Parameters
        ----------
        json_file : str
            location of json file
        img_dir : str
            path to directory of original images
        out_dir : str
            path to output directory
        """
        self.img_dir = Path(img_dir)
        self.out_dir = Path(out_dir)
        self.data = self.prepare_df(json_file)  # Allows inspection of DF.

    def prepare_df(self, json_file: str) -> pd.DataFrame:
        """Prepare dataframe for output.
        """
        json_df = pd.read_json(json_file).T
        df = (
            pd.concat(
                {i: pd.json_normalize(x) for i, x in json_df.pop("regions").items()}
            )
            .reset_index(level=1, drop=True)
            .join(json_df)
            .reset_index(drop=True)
        )  # Normalize json data to one node depth.

        df.rename(
            columns={
                "shape_attributes.all_points_x": "x_points",
                "shape_attributes.all_points_y": "y_points",
                "region_attributes.Type": "type",
            },
            inplace=True,
        )
        df.drop(
            ["shape_attributes.name", "size", "file_attributes"], axis=1, inplace=True,
        )
        df[["filename", "filetype"]] = df["filename"].str.split(".", expand=True)
        df["count"] = (
            df.groupby(["filename", "type"]).cumcount().astype(str)
        )  # For identifier at end of output file name, avoids overwriting files
        df = df[["filename", "x_points", "y_points", "type", "filetype", "count"]]
        return df

    def create_images(self) -> None:
        """Generate mask images into specifed output directory.
        """
        df = self.data
        for index, row in df.iterrows():
            og_img = f"{row['filename']}.{row['filetype']}"
            width, height = Image.open(self.img_dir / og_img).size
            coords = [
                point for point in zip(row["x_points"], row["y_points"])
            ]  # (x, y)
            image = Image.new("1", (width, height))  # Change to "RGB" for colour.
            draw = ImageDraw.Draw(image)
            draw.polygon((coords), fill="white")
            out_file_type = ".png"
            filename = row[["filename", "type", "count"]].values.tolist()
            filename[-1] += out_file_type
            # <filename>_<class/type>_<count>.<out_file_type>
            out_img_name = "_".join(filter(None, filename))
            # You can specify image format by img.save(<path>, "<filetype>")
            image.save(self.out_dir / out_img_name)
