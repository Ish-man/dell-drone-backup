 /* -*- c++ -*- */
/*
 * Copyright 2020 gr-iridium author.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "iuchar_to_complex_impl.h"
#include <iostream>
#include <boost/asio.hpp>


#include <gnuradio/io_signature.h>
#include <gnuradio/prefs.h>

// #include <qwt_symbol.h>
#include <chrono>
#include <iomanip>
#include <volk/volk.h>

#include <algorithm>
#include <cstring>

namespace gr {
namespace iridium {

iuchar_to_complex::sptr iuchar_to_complex::make()
{
    return gnuradio::get_initial_sptr(new iuchar_to_complex_impl());
}


/*
 * The private constructor
 */
iuchar_to_complex_impl::iuchar_to_complex_impl()
    : gr::sync_decimator("iuchar_to_complex",
                         gr::io_signature::make(1, 1, sizeof(gr_complex )),
                         gr::io_signature::make(1, 1, sizeof(gr_complex)),
                         1)
{
    //set_output_multiple(4096);
    start_flag = 0; s_cycle=0;
    freq_flag = 0;
    meanVec_flag = 0;
    ch_flag = 0;
    oneCount = 0;
    chCounter = -1;
    chCounter1 = 0;
    meanVecCount=0;
    
    local_meanVec = (gr_complex*) malloc (sizeof(gr_complex)*16384);
    local_ch_idx = (gr_complex*) malloc (sizeof(gr_complex)*16384);
    local_ch_cen = (gr_complex*) malloc (sizeof(gr_complex)*16384);
    local_ch_mag = (gr_complex*) malloc (sizeof(gr_complex)*16384);
    local_ch_bw = (gr_complex*) malloc (sizeof(gr_complex)*16384);
    
    csv_file.open("output.csv", std::ios::trunc | std::ios::out );
    if (!csv_file.is_open()) {
        throw std::runtime_error("Failed to open CSV file for writing");
    }
    csv_file << "time,location,channel frequency, channel magnitude, channel bandwidth\n";
}

/*
 * Our virtual destructor.
 */
iuchar_to_complex_impl::~iuchar_to_complex_impl() {

    free (local_meanVec);
    free (local_ch_idx);
    free (local_ch_cen);
    free (local_ch_mag);
    free (local_ch_bw);
    
    if (csv_file.is_open()) {
        csv_file.close();
    }
}

int iuchar_to_complex_impl::work(int noutput_items,
                                 gr_vector_const_void_star& input_items,
                                 gr_vector_void_star& output_items)
{
    const gr_complex* in = (const gr_complex*)input_items[0];
    gr_complex* out = (gr_complex*)output_items[0];
    
    for (int i = 0; i <= noutput_items-1; ++i){ 
    
           if(start_flag==0 && in[i]==gr_complex(1,0)) {
        	start_flag=1; 
        	oneCount++;     //  std::cout<<s_cycle+i<<" first "<<i<<"  "<<noutput_items<<"  "<<in[i-1]<<"  "<<in[i]<<"  "<<in[i+1]<<"\n";    	
        }
        
        else if(start_flag==1 && in[i]==gr_complex(1,0) && ch_flag == 0) {
        	oneCount++;
        	if(oneCount==16383){
							// std::cout<<s_cycle+i<<" second "<<i<<"  "<<noutput_items<<"  "<<in[i-1]<<"  "<<in[i]<<"  "<<in[i+1]<<"\n";
                freq_flag=1;
        	}
        }
        
        else if(freq_flag==1 && start_flag==1){
            local_freq = in[i];  	// std::cout<<s_cycle+i<<" third "<<i<<"  "<<noutput_items<<"  "<<local_freq<<"  "<<in[i-1]<<"  "<<in[i]<<"  "<<in[i+1]<<"\n";
        	meanVec_flag=1;	 //  std::cout<<local_freq.real()<<"\n";
        	freq_flag=0;
        }
        
        else if(meanVec_flag==1 && start_flag==1){
        	local_meanVec[meanVecCount]=in[i];
        	meanVecCount++;
        	if(meanVecCount==16384){	//  std::cout<<s_cycle+i<<"  "<<i<<"  "<<noutput_items<<" fourth "<<local_freq<<"  "<< local_meanVec[0] <<"  "<<local_meanVec[1] <<"  "<<in[i-1]<<"  "<<in[i]<<"  "<<in[i+2]<<"\n";
        		ch_flag=1;
        		meanVec_flag=0;
        	}
        }
        else if (ch_flag == 1 && start_flag == 1 && chCounter == -1){
            total_chs = in[i].real();		//  std::cout<<s_cycle+i<<" fifth "<<i<<"  "<<total_chs<<"  "<<in[i-1]<<"  "<<in[i]<<"  "<<in[i+1]<<"\n";
            chCounter++;
            if(total_chs==0){			//  std::cout<<total_chs<<" dummy_fifth "<<local_freq<<"\n";
                ch_flag = 0;
                start_flag = 0;
                oneCount = 0;
                meanVecCount= 0;
                chCounter = -1;  
                local_freq = -1;   
            
            }
        } 

        else if (ch_flag == 1 && start_flag == 1 && chCounter >= 0){	
            if(chCounter1==0) { local_ch_idx[chCounter] = in[i]; chCounter1++;}
            else if(chCounter1==1) { local_ch_cen[chCounter] = in[i]; chCounter1++;}
            else if(chCounter1==2) { local_ch_mag[chCounter] = in[i]; chCounter1++;}
            else if(chCounter1==3) {
                local_ch_bw[chCounter] = in[i];	    
                //std::cout<<total_chs<<" dummy_sixth "<<local_freq<<"  "<<local_ch_idx[chCounter]<<" "<<local_ch_cen[chCounter]<<"  "<<local_ch_mag[chCounter]<<"  "<<local_ch_bw[chCounter] <<"\n";
                
                auto now = std::chrono::system_clock::now();
                std::time_t now_time = std::chrono::system_clock::to_time_t(now);
                auto now_ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;

                std::ostringstream oss;
                oss << std::put_time(std::localtime(&now_time), "%Y-%m-%d %H:%M:%S");
                oss << '.' << std::setfill('0') << std::setw(3) << now_ms.count();

                
                csv_file << oss.str() << ","                // time
                << chCounter << ","                // location 
                << local_ch_cen[chCounter].real() << ","        // channel_freq
                << local_ch_mag[chCounter].real() << "," // channel_magnitude
                << local_ch_bw[chCounter].real() << "\n";
                chCounter1 = 0;			
                chCounter++;
                if(chCounter == total_chs){		// std::cout<<s_cycle+i<<" sixth "<<i<<"  "<<noutput_items<<"  "<<chCounter<<"  "<<in[i-1]<<"  "<<in[i]<<"  "<<in[i+1]<<"\n";

                      
                    ch_flag = 0;
                    start_flag = 0;
                    oneCount = 0;		
                    meanVecCount= 0;
                    chCounter = -1;
                    local_freq = -1;  
                }
            }

        }		

        }
        
        s_cycle+= noutput_items; 
        
        memcpy(out, in , sizeof(gr_complex) * noutput_items);
               

    // Tell runtime system how many output items we produced.
    return noutput_items;
}

} /* namespace iridium */
} /* namespace gr */
