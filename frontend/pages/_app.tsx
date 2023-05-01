import type { AppProps } from 'next/app'
import { NextUIProvider, createTheme } from '@nextui-org/react'
import { ThemeProvider as NextThemeProvider} from 'next-themes';

export default function App({ Component, pageProps }: AppProps) {
    // Themes
    const lightTheme = createTheme({
      type: 'dark',
      theme: {
      colors: {}, // optional
      }
  })

  const darkTheme = createTheme({
      type: 'dark',
      theme: {
      colors: {}, // optional
      }
  })
  
  return <NextThemeProvider
    defaultTheme="system"
    attribute="class"
    value={{
        light: lightTheme.className,
        dark: darkTheme.className
    }}
  >
    <NextUIProvider>
      <Component {...pageProps} />
    </NextUIProvider>
  </NextThemeProvider>
}
