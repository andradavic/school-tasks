import { SafeAreaView } from "react-native-safe-area-context";
import { StatusBar } from "expo-status-bar";
import {
  useFonts,
  NunitoSans_400Regular,
  NunitoSans_600SemiBold,
  NunitoSans_700Bold,
} from "@expo-google-fonts/nunito-sans";

import { Routes } from "./routes";
import { AuthContextProvider } from "./context/auth";
import { ErrorModalContextProvider } from "./context/error-modal";

import * as SplashScreen from "expo-splash-screen";

import "./utils/dayjs";

SplashScreen.preventAutoHideAsync();

export default function App() {
  let [fontsLoaded] = useFonts({
    NunitoSans_400Regular,
    NunitoSans_600SemiBold,
    NunitoSans_700Bold,
  });

  if (!fontsLoaded) {
    return null;
  }

  return (
    <SafeAreaView className="flex-1 bg-background">
      <ErrorModalContextProvider>
        <AuthContextProvider>
          <Routes />
        </AuthContextProvider>
      </ErrorModalContextProvider>

      <StatusBar style="light" backgroundColor="#18181b" />
    </SafeAreaView>
  );
}
