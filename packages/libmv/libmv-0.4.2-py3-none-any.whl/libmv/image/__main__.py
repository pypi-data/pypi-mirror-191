import json
import os
from typing import Any

import colortool
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from musictool.note import WHITE_NOTES
from musictool.note import SpecificNote
from musictool.noterange import NoteRange
from musictool.pitch import Pitch
from musictool.scale import Scale
from PIL import Image
from PIL import ImageDraw

from libmv.config import IMAGE_CONFIG
from libmv.util import Track
from extraredis._sync import ExtraRedis

matplotlib.use('Agg')


class Images:
    def __init__(self, track_id: str, config: dict[str, Any] | None = None):
        self.track = Track(track_id)
    
        self.extraredis = ExtraRedis.from_url(os.environ['REDIS_URL'], decode_responses=True)
        self.meta = json.loads(self.extraredis.redis.get(self.track.meta))
        self.pitch = json.loads(self.extraredis.redis.get(self.track.pitch))

        self.seconds = self.meta['seconds']
        self.config = IMAGE_CONFIG.copy() if config is None else config

        self.n_screens = self.seconds / self.config['seconds_per_screen']
        self.height_no_pad = self.n_screens * self.config['height']
        self.height = self.height_no_pad + self.config['height']  # add one screen as padding
        self.minimap_width = int(self.config['width'] * self.config['minimap_width_percent'])
        self.minimap_box_height = int(self.config['height'] / (self.n_screens + 1))  # minimap box height
        self.main_width = self.config['width'] - self.minimap_width  # width of main image (without minimap)

        self.ph = Pitch()
        self.scale = Scale.from_name(self.config['scale_root'], self.config['scale_name'])
        self.nr = NoteRange(SpecificNote.from_str(self.config['note_min']), SpecificNote.from_str(self.config['note_max']))
        self.hz_min, self.hz_max = self.ph.note_i_to_hz(self.nr[0].i - 0.5), self.ph.note_i_to_hz(self.nr[-1].i + 0.5)

        self.config['minimap_box_height'] = self.minimap_box_height
        self.config['minimap_width'] = self.minimap_width
        self.config['main_width'] = self.main_width
        self.meta['image'] = self.config

    def __call__(self):
        self.image_pitch()
        self.image_minimap()
        self.image_minimapbox()
        self.image_piano()
        self.image_label()
        self.image_background()
        self.update_meta()

    def update_meta(self):
        self.extraredis.redis.set(self.track.meta, json.dumps(self.meta))

    def image_pitch(
        self,
        width: int | None = None,
        height: int | None = None,
        filename: str | None = None,
        minimap_pad: bool = True,
    ):
        width = self.main_width if width is None else width
        height = self.height if height is None else height
        filename = self.track.image_pitch if filename is None else filename

        fig, ax = plt.subplots(
            1, 1,
            # figsize=(self.main_width / self.config['dpi'], self.height / self.config['dpi']),
            figsize=(width / self.config['dpi'], height / self.config['dpi']),
            frameon=False,
            dpi=self.config['dpi'],
        )

        for k, v in self.pitch.items():
            linewidth = 1.5 if k == 'mean' else 0.25
            color = 'black' if k == 'mean' else None
            ax.plot(v['f0'], v['t'], linewidth=linewidth, color=color, label=k)

        # add word labels
        for word in self.meta['words']:
            text = '\n'.join([
                f"word_index: {word['word_index']}",
                f"duration {word['duration']:.1f}",
                f"closest_note {word['closest_note']}",
                f"std_log2 {word['std_log2']:.5f}",
                f"mae_log2 {word['mae_log2']:.5f}",
                f"rmse_log2 {word['rmse_log2']:.5f}",
            ])
            ax.text(word['f0_start'], word['t_start'], text, ha='left', va='bottom', fontsize=32, color='black', fontdict={'family': 'monospace'})

        ax.grid(axis='y', lw=5)
        ax.semilogx()
        ax.set_ylim(0 - self.config['seconds_per_screen'] / 2, self.seconds + self.config['seconds_per_screen'] / 2)
        ax.set_xlim(self.hz_min, self.hz_max)

        fig.subplots_adjust(bottom=0, top=1, right=1, left=0)
        plt.savefig(filename, transparent=True)

        if minimap_pad:
            pitch = Image.open(filename)
            out = Image.fromarray(np.zeros((pitch.size[1], self.config['width'], 4), dtype=np.uint8))
            out.paste(pitch, (0, 0), pitch)
            out.save(filename)

    def image_minimap(self):
        fig, ax = plt.subplots(
            1, 1,
            figsize=(self.minimap_width / self.config['dpi'], self.config['height'] / self.config['dpi']),
            frameon=False,
            dpi=self.config['dpi'],
        )

        for k, v in self.pitch.items():
            linewidth = 1.5 if k == 'mean' else 0.25
            color = 'black' if k == 'mean' else None
            ax.plot(v['f0'], v['t'], linewidth=linewidth, color=color, label=k)
        ax.grid(axis='y')

        ax.semilogx()
        ax.set_ylim(0 - self.config['seconds_per_screen'] / 2, self.seconds + self.config['seconds_per_screen'] / 2)
        ax.set_xlim(self.hz_min, self.hz_max)
        fig.subplots_adjust(bottom=0, top=1, right=1, left=0)
        plt.savefig(self.track.image_minimap)

    def image_minimapbox(self):
        box_a = np.zeros((self.minimap_box_height, self.minimap_width, 4), dtype=np.uint8)
        box_a[:, :, 0] = 0xFF
        box_a[:, :, 3] = 0x64
        box = Image.fromarray(box_a)
        draw = ImageDraw.Draw(box)
        mid = box.size[1] // 2
        draw.line((0, mid, box.size[0], mid), fill=(255, 0, 0, 255))
        box.save(self.track.image_minimapbox)

    def image_piano(
        self,
        width: int | None = None,
        height: int | None = None,
        filename: str | None = None,
    ):
        width = self.main_width if width is None else width
        height = self.config['height'] if height is None else height
        filename = self.track.image_piano if filename is None else filename

        fig, ax = plt.subplots(
            1, 1,
            figsize=(width / self.config['dpi'], height / self.config['dpi']),
            frameon=False,
            dpi=self.config['dpi'],
        )
        ax.semilogx()
        ax.set_xlim(self.hz_min, self.hz_max)
        ax.set_ylim(0, 1)
        ax.set_facecolor(colortool.WHITE_BRIGHT.css_hex)

        SQUARE_MARGIN = 0.075
        SCALE_RECT_HEIGHT = width / len(self.nr) * (1 - 2 * SQUARE_MARGIN) / height

        for n in self.nr:
            n_start_hz = self.ph.note_i_to_hz(n.i - 0.5)
            n_stop_hz = self.ph.note_i_to_hz(n.i + 0.5)
            n_start_hz_margin = self.ph.note_i_to_hz(n.i - 0.5 + SQUARE_MARGIN)
            n_stop_hz_margin = self.ph.note_i_to_hz(n.i + 0.5 - SQUARE_MARGIN)

            na = n.abstract

            BLACK = colortool.Color.from_hex(0xDDDDDD)
            color = colortool.WHITE_BRIGHT if na in WHITE_NOTES else BLACK

            ax.add_patch(
                Rectangle(
                    (n_start_hz, 0), n_stop_hz - n_start_hz, 1, linewidth=1,
                    # edgecolor='k',
                    edgecolor=BLACK.css_hex,
                    facecolor=color.css_hex,
                    fill=True,
                ),
            )

            if na in self.scale:
                pass
                # ax.add_patch(
                #     Rectangle(
                #         (n_start_hz, 0), n_stop_hz - n_start_hz, 1, linewidth=1, edgecolor='k', facecolor='#FF000020',
                #         fill=True,
                #     ),
                # )

                ax.add_patch(
                    Rectangle(
                        (n_start_hz_margin, 0.5 - SCALE_RECT_HEIGHT / 2), n_stop_hz_margin - n_start_hz_margin, SCALE_RECT_HEIGHT, linewidth=1,
                        # edgecolor='#FF000020',
                        # edgecolor='red',
                        # edgecolor='#CCCCCC',
                        # facecolor='#FF000020',
                        facecolor='#FF000040',
                        # facecolor='#ffd8db10',
                        fill=True,
                        # fill=False,
                        # hatch='.',
                    ),
                )

        fig.subplots_adjust(bottom=0, top=1, right=1, left=0)
        plt.savefig(filename)

    def image_label(
        self,
        width: int | None = None,
        height: int | None = None,
        filename: str | None = None,
    ):
        width = self.main_width if width is None else width
        height = self.config['height'] if height is None else height
        filename = self.track.image_labels if filename is None else filename

        fig, ax = plt.subplots(
            1, 1,
            figsize=(width / self.config['dpi'], height / self.config['dpi']),
            frameon=False,
            dpi=self.config['dpi'],
        )
        ax.set_xlim(self.hz_min, self.hz_max)

        y_ticks, y_labels = [], []

        for n in self.nr:
            hz = self.ph.note_to_hz(n)

            if n.abstract in self.scale.notes:
                if n.abstract == self.scale.root:
                    lw = 5
                    linestyle = '-'
                else:
                    lw = 0.9
                    linestyle = '--'

                color = 'red'
                y_ticks.append(hz)
                y_labels.append(f'{self.scale.note_to_interval[n.abstract]}\n{n}\n{hz:.0f} Hz')
            else:
                # lw = 0.25
                lw = 0.2
                linestyle = (0, (5, 10))
                color = 'black'

            # anyway
            lw = 0.25
            linestyle = (0, (5, 10))
            color = 'black'

            #     ax.axvline(hz, ymin=0.49, ymax=0.51, color='k', lw=lw)
            ax.axvline(hz, color=color, lw=lw, linestyle=linestyle)

        ax.axhline(0.5, color='r')

        ax.semilogx()
        ax.set_yticks([], [], minor=True)
        ax.set_yticks([], [], minor=False)
        ax.set_xticks([], [], minor=True)
        ax.set_xticks(y_ticks, y_labels, fontsize=15, fontname='monospace')

        ax.xaxis.set_tick_params(direction='in', which='both', pad=-50)

        ax.grid(lw=0.3, axis='y')
        ax.set_title(f'{self.scale.root.name} {self.scale.name}', y=0.98, fontsize=24)

        fig.subplots_adjust(bottom=0, top=1, right=1, left=0)
        plt.savefig(filename, transparent=True)

    def image_background(self, single: bool = False):
        """make background image from piano, labels and pitch (optional)"""
        if single:
            piano_file = self.track.single_image_piano
            label_file = self.track.single_image_labels
            filename = self.track.single_image_background
        else:
            piano_file = self.track.image_piano
            label_file = self.track.image_labels
            filename = self.track.image_background

        piano = Image.open(piano_file)
        label = Image.open(label_file)
        assert piano.size == label.size
        piano.paste(label, (0, 0), label)

        if single:
            width, height = piano.size
            # libx264 requires even width and height
            if width % 2 != 0:
                width += 1
            if height % 2 != 0:
                height += 1
        else:
            width, height = self.config['width'], self.config['height']

        out = Image.fromarray(np.zeros((height, width, 4), dtype=np.uint8))
        out.paste(piano, (0, 0), piano)
        if single:
            pitch = Image.open(self.track.single_image_pitch)
            out.paste(pitch, (0, 0), pitch)
            # GPU limitation. Wont resize if size is less than max allowed
            out.thumbnail((self.config['single_max_width'], self.config['single_max_height']))
        else:
            minimap = Image.open(self.track.image_minimap)
            out.paste(minimap, (piano.size[0], 0), minimap)
        out.save(filename)

    def single_image(self):
        self.image_pitch(width=self.config['width'], height=self.height, filename=self.track.single_image_pitch)
        self.image_piano(width=self.config['width'], height=self.height, filename=self.track.single_image_piano)
        self.image_label(width=self.config['width'], height=self.height, filename=self.track.single_image_labels)
        self.image_background(single=True)


def main(track_id: str, config: str | None = None, single: bool = False):
    im = Images(track_id, config)
    if single:
        im.single_image()
    else:
        im()


# @click.command()
# @click.option('--track-id', type=str, required=True, help='id of track to process')
# @click.option('--config', type=str, required=False, help='path to config file')
# def _main(metadatafile: str, config: str | None):
#     main(metadatafile, config)
#
#
# if __name__ == '__main__':
#     _main()
