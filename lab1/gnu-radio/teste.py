#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class teste(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "teste")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 768e3
        self.noise_level = noise_level = 100e-3
        self.a3 = a3 = 0
        self.a2 = a2 = 0
        self.a1 = a1 = 1

        ##################################################
        # Blocks
        ##################################################

        self._noise_level_range = qtgui.Range(0, 300e-3, 5e-3, 100e-3, 200)
        self._noise_level_win = qtgui.RangeWidget(self._noise_level_range, self.set_noise_level, "'noise_level'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_level_win)
        self._a3_range = qtgui.Range(0, 1, 200e-3, 0, 200)
        self._a3_win = qtgui.RangeWidget(self._a3_range, self.set_a3, "'a3'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._a3_win)
        self._a2_range = qtgui.Range(0, 1, 200e-3, 0, 200)
        self._a2_win = qtgui.RangeWidget(self._a2_range, self.set_a2, "'a2'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._a2_win)
        self._a1_range = qtgui.Range(0, 2, 200e-3, 1, 200)
        self._a1_win = qtgui.RangeWidget(self._a1_range, self.set_a1, "'a1'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._a1_win)
        self.qtgui_number_sink_snr = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_snr.set_update_time(0.10)
        self.qtgui_number_sink_snr.set_title('SNR(dB)')

        labels = ['SNR', '', '', '', '',
            '', '', '', '', '']
        units = ['dB', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_snr.set_min(i, -1)
            self.qtgui_number_sink_snr.set_max(i, 1)
            self.qtgui_number_sink_snr.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_snr.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_snr.set_label(i, labels[i])
            self.qtgui_number_sink_snr.set_unit(i, units[i])
            self.qtgui_number_sink_snr.set_factor(i, factor[i])

        self.qtgui_number_sink_snr.enable_autoscale(True)
        self._qtgui_number_sink_snr_win = sip.wrapinstance(self.qtgui_number_sink_snr.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_snr_win)
        self.qtgui_number_sink_snr.set_block_alias("SNR")
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'FFT plot', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['Rx Signal', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_freq_sink_x_0.set_block_alias("Rx signal")
        self.low_pass_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                25e3,
                500,
                window.WIN_BLACKMAN,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                25e3,
                500,
                window.WIN_BLACKMAN,
                6.76))
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\Tomas\\Desktop\\uni\\5th\\1st_sem\\csrf\\lab\\github\\csrf\\lab1\\gnu-radio\\pedro.wav', True)
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_rms_xx_1 = blocks.rms_ff(0.0001)
        self.blocks_rms_xx_0 = blocks.rms_ff(0.0001)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(20, 1, 0)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0_2 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_0_1_1 = blocks.multiply_const_cc(a3)
        self.blocks_multiply_const_vxx_0_1_0 = blocks.multiply_const_cc(a2)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_cc(a1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1)
        self.blocks_float_to_complex_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_exponentiate_const_cci_0_0 = blocks.exponentiate_const_cci(3, 1)
        self.blocks_exponentiate_const_cci_0 = blocks.exponentiate_const_cci(2, 1)
        self.blocks_divide_xx_1 = blocks.divide_ff(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_float_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(1)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_sig_source_x_1_0_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 75e3, 1, 0, 0)
        self.analog_sig_source_x_1_0_0_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, 75e3, 1, 0, 0)
        self.analog_sig_source_x_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 75e3, 1, 0, 0)
        self.analog_noise_source_x_0_0 = analog.noise_source_f(analog.GR_GAUSSIAN, noise_level, 0)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, noise_level, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0_0, 1))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_rms_xx_1, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.analog_sig_source_x_1_0_0_0, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.analog_sig_source_x_1_0_1, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0_2, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_complex_to_float_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_rms_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_divide_xx_1, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_exponentiate_const_cci_0, 0), (self.blocks_multiply_const_vxx_0_1_0, 0))
        self.connect((self.blocks_exponentiate_const_cci_0_0, 0), (self.blocks_multiply_const_vxx_0_1_1, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_exponentiate_const_cci_0, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_exponentiate_const_cci_0_0, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_float_to_complex_1, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1_1, 0), (self.blocks_add_xx_1, 2))
        self.connect((self.blocks_multiply_const_vxx_0_2, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_2, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_number_sink_snr, 0))
        self.connect((self.blocks_rms_xx_0, 0), (self.blocks_divide_xx_1, 0))
        self.connect((self.blocks_rms_xx_1, 0), (self.blocks_divide_xx_1, 1))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_float_to_complex_1, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_float_to_complex_1, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "teste")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1_0_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1_0_1.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 25e3, 500, window.WIN_BLACKMAN, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 25e3, 500, window.WIN_BLACKMAN, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_noise_level(self):
        return self.noise_level

    def set_noise_level(self, noise_level):
        self.noise_level = noise_level
        self.analog_noise_source_x_0.set_amplitude(self.noise_level)
        self.analog_noise_source_x_0_0.set_amplitude(self.noise_level)

    def get_a3(self):
        return self.a3

    def set_a3(self, a3):
        self.a3 = a3
        self.blocks_multiply_const_vxx_0_1_1.set_k(self.a3)

    def get_a2(self):
        return self.a2

    def set_a2(self, a2):
        self.a2 = a2
        self.blocks_multiply_const_vxx_0_1_0.set_k(self.a2)

    def get_a1(self):
        return self.a1

    def set_a1(self, a1):
        self.a1 = a1
        self.blocks_multiply_const_vxx_0_1.set_k(self.a1)




def main(top_block_cls=teste, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
