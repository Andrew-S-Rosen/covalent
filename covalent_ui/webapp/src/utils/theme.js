/**
 * Copyright 2021 Agnostiq Inc.
 *
 * This file is part of Covalent.
 *
 * Licensed under the GNU Affero General Public License 3.0 (the "License").
 * A copy of the License may be obtained with this software package or at
 *
 *      https://www.gnu.org/licenses/agpl-3.0.en.html
 *
 * Use of this file is prohibited except in compliance with the License. Any
 * modifications or derivative works of this file must retain this copyright
 * notice, and modified files must contain a notice indicating that they have
 * been altered from the originals.
 *
 * Covalent is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the License for more details.
 *
 * Relief from the License may be granted by purchasing a commercial license.
 */

import React from 'react'
import { createTheme } from '@mui/material/styles'
import { Link as RouterLink } from 'react-router-dom'

const LinkBehavior = React.forwardRef(({ href, ...props }, ref) => {
  // Map href (MUI) -> to (react-router)
  return <RouterLink ref={ref} to={href} {...props} />
})

const defaultTheme = createTheme({
  typography: {
    fontFamily: '"Roboto Slab", "Helvetica", "Arial", sans-serif',
  },
  palette: {
    mode: 'dark',
    primary: {
      main: '#99DAFF',
    },
    secondary: {
      main: '#998AFF',
    },
    background: {
      default: '#040406',
      paper: '#101820',
    },
    error: {
      main: '#E35050',
    },
    success: {
      main: '#64F4D2',
    },
    warning: {
      main: '#E39F50',
    },
  },
})

const theme = createTheme(defaultTheme, {
  components: {
    MuiLink: {
      defaultProps: {
        component: LinkBehavior,
      },
    },
    MuiButtonBase: {
      defaultProps: {
        LinkComponent: LinkBehavior,
      },
    },
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          // adapted from @mui/material/darkScrollbar
          scrollbarColor: '#6b6b6b #2b2b2b',
          '&::-webkit-scrollbar, & *::-webkit-scrollbar': {
            backgroundColor: '#2b2b2b',
            height: 6,
            width: 6,
          },
          '&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb': {
            borderRadius: 8,
            backgroundColor: '#6b6b6b',
            minHeight: 24,
            // border: '2px solid #2b2b2b',
          },
          '&::-webkit-scrollbar-thumb:focus, & *::-webkit-scrollbar-thumb:focus':
            {
              backgroundColor: '#959595',
            },
          '&::-webkit-scrollbar-thumb:active, & *::-webkit-scrollbar-thumb:active':
            {
              backgroundColor: '#959595',
            },
          '&::-webkit-scrollbar-thumb:hover, & *::-webkit-scrollbar-thumb:hover':
            {
              backgroundColor: '#959595',
            },
          '&::-webkit-scrollbar-corner, & *::-webkit-scrollbar-corner': {
            backgroundColor: '#2b2b2b',
          },
        },
      },
    },
    // MuiTabs: {
    //   styleOverrides: {
    //     root: {
    //       '& .MuiTabs-indicator': {
    //         backgroundColor: defaultTheme.palette.text.primary,
    //         height: 1,
    //       },
    //     },
    //   },
    // },
    // MuiTab: {
    //   styleOverrides: {
    //     root: {
    //       textTransform: 'none',
    //       '&.Mui-selected': {
    //         color: defaultTheme.palette.text.primary,
    //       },
    //     },
    //   },
    // },
  },
})

export default theme