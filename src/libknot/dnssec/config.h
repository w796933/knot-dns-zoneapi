/*  Copyright (C) 2013 CZ.NIC, z.s.p.o. <knot-dns@labs.nic.cz>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
/*!
 * \file config.h
 *
 * \author Jan Vcelak <jan.vcelak@nic.cz>
 *
 * \brief DNSSEC configuration for Knot DNS.
 *
 * \addtogroup dnssec
 * @{
 */

#pragma once

#include <openssl/opensslconf.h>
#include <openssl/opensslv.h>

#ifndef OPENSSL_VERSION_NUMBER
#error "OpenSSL version is not defined."
#endif

// ECDSA support requires OpenSSL version >= 1.0.1
#if !defined(OPENSSL_NO_ECDSA) && OPENSSL_VERSION_NUMBER >= 0x10001000L
  #define KNOT_ENABLE_ECDSA 1
#else
  #undef KNOT_ENABLE_ECDSA
#endif

#if !defined(OPENSSL_NO_GOST) && OPENSSL_VERSION_NUMBER >= 0x1000001fL
  #define KNOT_ENABLE_GOST 1
#else
  #undef KNOT_ENABLE_GOST
#endif

/*! @} */
