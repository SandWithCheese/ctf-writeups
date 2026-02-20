#include "out.h"

ulonglong FUN_140001180(undefined *param_1, undefined *param_2,
                        undefined8 param_3, undefined8 param_4)

{
  int iVar1;
  longlong lVar2;
  bool bVar3;
  uint uVar4;
  longlong lVar5;
  undefined8 *puVar6;
  size_t sVar7;
  void *_Dst;
  ulonglong uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  longlong lVar11;
  size_t _Size;
  undefined8 *puVar12;
  undefined8 in_R9;
  longlong unaff_GS_OFFSET;

  lVar2 = *(longlong *)(*(longlong *)(unaff_GS_OFFSET + 0x30) + 8);
  while (true) {
    LOCK();
    lVar11 = 0;
    lVar5 = lVar2;
    if (DAT_14000e040 != 0) {
      lVar11 = DAT_14000e040;
      lVar5 = DAT_14000e040;
    }
    DAT_14000e040 = lVar5;
    UNLOCK();
    if (lVar11 == 0)
      break;
    if (lVar2 == lVar11) {
      bVar3 = true;
    joined_r0x0001400011db:
      if (DAT_14000e048 == 1) {
        _amsg_exit(0x1f);
      } else if (DAT_14000e048 == 0) {
        DAT_14000e048 = 1;
        _initterm();
      } else {
        DAT_14000e008 = 1;
      }
      if (DAT_14000e048 == 1) {
        _initterm();
        DAT_14000e048 = 2;
      }
      if (!bVar3) {
        LOCK();
        DAT_14000e040 = 0;
        UNLOCK();
      }
      uVar10 = 2;
      uVar9 = 0;
      tls_callback_0(0, 2);
      FUN_140001ca0(uVar9, uVar10, param_3, param_4);
      DAT_14000e0d0 = SetUnhandledExceptionFilter(
          (LPTOP_LEVEL_EXCEPTION_FILTER)&LAB_140002050);
      FUN_1400078d0(&LAB_140001000);
      FUN_140001ab0();
      uVar4 = DAT_14000e028;
      iVar1 = DAT_14000e028 + 1;
      _Size = (longlong)iVar1 * 8;
      puVar6 = (undefined8 *)malloc(_Size);
      lVar2 = (longlong)DAT_14000e020;
      puVar12 = puVar6;
      if (0 < (int)uVar4) {
        lVar11 = 0;
        do {
          sVar7 = strlen(*(char **)(lVar2 + lVar11));
          _Dst = malloc(sVar7 + 1);
          *(void **)((longlong)puVar6 + lVar11) = _Dst;
          puVar12 = (undefined8 *)(lVar2 + lVar11);
          lVar11 = lVar11 + 8;
          memcpy(_Dst, (void *)*puVar12, sVar7 + 1);
        } while (_Size - 8 != lVar11);
        puVar12 = puVar6 + (longlong)iVar1 + -1;
      }
      *puVar12 = 0;
      DAT_14000e020 = puVar6;
      FUN_1400018b0();
      uVar9 = DAT_14000e018;
      uVar8 = (ulonglong)DAT_14000e028;
      *(undefined8 *)__initenv_exref = DAT_14000e018;
      uVar8 = FUN_140001575(uVar8, DAT_14000e020, uVar9, in_R9);
      DAT_14000e010 = (uint)uVar8;
      if (DAT_14000e00c != 0) {
        if (DAT_14000e008 != 0) {
          return uVar8;
        }
        _cexit();
        return (ulonglong)DAT_14000e010;
      }
      // WARNING: Subroutine does not return
      exit(DAT_14000e010);
    }
    Sleep(1000);
  }
  bVar3 = false;
  goto joined_r0x0001400011db;
}

void entry(undefined *param_1, undefined *param_2, undefined8 param_3,
           undefined8 param_4)

{
  DAT_14000e090 = 0;
  FUN_140001180(param_1, param_2, param_3, param_4);
  return;
}

int FUN_140001410(_onexit_t param_1)

{
  _onexit_t p_Var1;

  p_Var1 = _onexit(param_1);
  return -(uint)(p_Var1 == (_onexit_t)0x0);
}

uint FUN_140001450(char *param_1, ulonglong param_2, undefined8 param_3,
                   undefined8 param_4)

{
  uint uVar1;
  FILE *pFVar2;
  ulonglong local_res10;
  undefined8 local_res18;
  undefined8 local_res20;

  local_res10 = param_2;
  local_res18 = param_3;
  local_res20 = param_4;
  pFVar2 = (FILE *)(*(code *)PTR_FUN_1400090b0)(1);
  uVar1 = FUN_1400028c0(pFVar2, param_1, &local_res10);
  return uVar1;
}

// WARNING: Globals starting with '_' overlap smaller symbols at the same
// address

void FUN_1400014a4(int param_1)

{
  LARGE_INTEGER local_30;
  LARGE_INTEGER local_28;
  LARGE_INTEGER local_20;
  float10 local_18;

  QueryPerformanceFrequency(&local_20);
  QueryPerformanceCounter(&local_28);
  local_18 = (float10)param_1 / _DAT_14000ac20;
  do {
    QueryPerformanceCounter(&local_30);
  } while ((float10)(local_30.QuadPart - (longlong)local_28) /
               (float10)local_20.QuadPart <
           local_18);
  return;
}

void FUN_14000151d(void)

{
  DWORD local_14;
  HANDLE local_10;

  local_10 = GetStdHandle(0xfffffff5);
  local_14 = 0;
  GetConsoleMode(local_10, &local_14);
  local_14 = local_14 | 4;
  SetConsoleMode(local_10, local_14);
  return;
}

undefined8 FUN_140001575(undefined8 param_1, undefined8 param_2,
                         undefined8 param_3, undefined8 param_4)

{
  int iVar1;
  undefined8 uVar2;
  longlong lVar3;
  undefined *puVar4;
  size_t _Count;
  undefined4 *puVar5;
  undefined8 *puVar6;
  byte *pbVar7;
  FILE *pFVar8;
  byte local_be8[4];
  undefined2 local_be4[1482];
  uint local_50;
  uint local_4c;
  uint local_48;
  byte local_41;
  ulonglong local_40;
  void *local_38;
  int local_2c;
  FILE *local_28;
  ulonglong local_20;

  FUN_1400018b0();
  FUN_14000151d();
  puVar4 = &DAT_14000a000;
  local_28 = fopen("program.banner", "rb");
  if (local_28 == (FILE *)0x0) {
    FUN_140001450("File containing banner ascii art is missing!\n",
                  (ulonglong)puVar4, param_3, param_4);
    uVar2 = 1;
  } else {
    fseek(local_28, 0, 2);
    local_2c = ftell(local_28);
    fseek(local_28, 0, 0);
    local_38 = malloc((longlong)local_2c);
    _Count = (size_t)local_2c;
    pFVar8 = local_28;
    fread(local_38, 1, _Count, local_28);
    fclose(local_28);
    puVar6 = (undefined8 *)&DAT_14000a080;
    pbVar7 = local_be8;
    for (lVar3 = 0x172; lVar3 != 0; lVar3 = lVar3 + -1) {
      *(undefined8 *)pbVar7 = *puVar6;
      puVar6 = puVar6 + 1;
      pbVar7 = pbVar7 + 8;
    }
    *(undefined4 *)pbVar7 = *(undefined4 *)puVar6;
    puVar5 = (undefined4 *)((longlong)puVar6 + 4);
    *(undefined2 *)(pbVar7 + 4) = *(undefined2 *)puVar5;
    local_40 = 0xb96;
    for (local_20 = 0; local_20 < local_40; local_20 = local_20 + 1) {
      _Count = (size_t)local_be8[local_20];
      puVar5 = (undefined4 *)(local_20 % (ulonglong)(longlong)local_2c);
      local_41 = *(byte *)((longlong)local_38 + (longlong)puVar5) ^
                 local_be8[local_20];
      if (local_41 == 0)
        break;
      iVar1 = (int)local_20;
      local_48 = iVar1 * 0x1e & 0xff;
      local_4c = iVar1 * -0xf + 0xffU & 0xff;
      local_50 = iVar1 * 0x3c & 0xff;
      pFVar8 = (FILE *)(ulonglong)local_50;
      _Count = (size_t)local_4c;
      puVar5 = (undefined4 *)(ulonglong)local_48;
      FUN_140001450("\x1b[38;2;%d;%d;%dm%c", (ulonglong)puVar5, _Count, pFVar8);
      FUN_1400014a4(5000);
    }
    FUN_140001450("\x1b[0m\n", (ulonglong)puVar5, _Count, pFVar8);
    free(local_38);
    FUN_140001450("Isn\'t it beautiful, my dear?\n", (ulonglong)puVar5, _Count,
                  pFVar8);
    _getch();
    uVar2 = 0;
  }
  return uVar2;
}

void FUN_140001840(void)

{
  int iVar1;
  ulonglong uVar2;
  ulonglong uVar3;
  undefined8 *puVar4;

  uVar2 = 0;
  do {
    uVar3 = uVar2;
    iVar1 = (int)uVar3;
    uVar2 = (ulonglong)(iVar1 + 1);
  } while ((&DAT_140007fe0)[iVar1 + 1] != 0);
  if (iVar1 != 0) {
    puVar4 = &DAT_140007fe0 + uVar3;
    do {
      (*(code *)*puVar4)();
      puVar4 = puVar4 + -1;
    } while (puVar4 !=
             (undefined8 *)(&UNK_140007fd8 + (uVar3 - (iVar1 - 1)) * 8));
  }
  FUN_140001410((_onexit_t)&LAB_140001800);
  return;
}

void FUN_1400018b0(void)

{
  if (DAT_14000e030 != 0) {
    return;
  }
  DAT_14000e030 = 1;
  FUN_140001840();
  return;
}

undefined8 FUN_1400018d0(void)

{
  return 0;
}

undefined8 tls_callback_1(undefined8 param_1, uint param_2)

{
  if ((param_2 != 3) && (param_2 != 0)) {
    return 1;
  }
  FUN_140002380(param_1, param_2);
  return 1;
}

// WARNING: Removing unreachable block (ram,0x000140001953)
// WARNING: Removing unreachable block (ram,0x000140001958)
// WARNING: Removing unreachable block (ram,0x000140001960)
// WARNING: Removing unreachable block (ram,0x000140001962)
// WARNING: Removing unreachable block (ram,0x00014000196b)

undefined8 tls_callback_0(undefined8 param_1, int param_2)

{
  if (DAT_140009020 != 2) {
    DAT_140009020 = 2;
  }
  if ((param_2 != 2) && (param_2 == 1)) {
    FUN_140002380(param_1, 1);
    return 1;
  }
  return 1;
}

void FUN_140001ab0(void)

{
  return;
}

void FUN_140001ac0(char *param_1, undefined8 param_2, undefined8 param_3,
                   undefined8 param_4)

{
  FILE *pFVar1;
  undefined8 local_res10;
  undefined8 local_res18;
  undefined8 local_res20;

  local_res10 = param_2;
  local_res18 = param_3;
  local_res20 = param_4;
  pFVar1 = FUN_1400078e0(2);
  fwrite("Mingw-w64 runtime failure:\n", 1, 0x1b, pFVar1);
  pFVar1 = FUN_1400078e0(2);
  vfprintf(pFVar1, param_1, (va_list)&local_res10);
  // WARNING: Subroutine does not return
  abort();
}

// WARNING: Removing unreachable block (ram,0x000140001d31)
// WARNING: Removing unreachable block (ram,0x000140001d3d)
// WARNING: Removing unreachable block (ram,0x000140001d47)
// WARNING: Removing unreachable block (ram,0x000140001d4a)
// WARNING: Removing unreachable block (ram,0x000140001d52)
// WARNING: Removing unreachable block (ram,0x000140001d5e)
// WARNING: Removing unreachable block (ram,0x000140001d6b)
// WARNING: Removing unreachable block (ram,0x000140001ddf)
// WARNING: Removing unreachable block (ram,0x000140001f08)
// WARNING: Removing unreachable block (ram,0x000140001f88)
// WARNING: Removing unreachable block (ram,0x000140001f92)
// WARNING: Removing unreachable block (ram,0x000140001f14)
// WARNING: Removing unreachable block (ram,0x000140001f2b)
// WARNING: Removing unreachable block (ram,0x000140001f34)
// WARNING: Removing unreachable block (ram,0x000140001f47)
// WARNING: Removing unreachable block (ram,0x000140001dfc)
// WARNING: Removing unreachable block (ram,0x000140001d80)
// WARNING: Removing unreachable block (ram,0x000140001d89)
// WARNING: Removing unreachable block (ram,0x000140001d92)
// WARNING: Removing unreachable block (ram,0x000140001f70)
// WARNING: Removing unreachable block (ram,0x000140001f7e)
// WARNING: Removing unreachable block (ram,0x000140001da4)
// WARNING: Removing unreachable block (ram,0x000140001db5)
// WARNING: Removing unreachable block (ram,0x000140001dbe)
// WARNING: Removing unreachable block (ram,0x000140001dc7)
// WARNING: Removing unreachable block (ram,0x000140001e60)
// WARNING: Removing unreachable block (ram,0x000140001f98)
// WARNING: Removing unreachable block (ram,0x000140001fa6)
// WARNING: Removing unreachable block (ram,0x000140001e72)
// WARNING: Removing unreachable block (ram,0x000140001e83)
// WARNING: Removing unreachable block (ram,0x000140001e8c)
// WARNING: Removing unreachable block (ram,0x000140001e92)
// WARNING: Removing unreachable block (ram,0x000140001eaa)
// WARNING: Removing unreachable block (ram,0x000140001dfe)
// WARNING: Removing unreachable block (ram,0x000140001fe2)
// WARNING: Removing unreachable block (ram,0x000140001ff0)
// WARNING: Removing unreachable block (ram,0x000140002014)
// WARNING: Removing unreachable block (ram,0x000140002039)
// WARNING: Removing unreachable block (ram,0x000140001e07)
// WARNING: Removing unreachable block (ram,0x000140001e1e)
// WARNING: Removing unreachable block (ram,0x000140001e23)
// WARNING: Removing unreachable block (ram,0x000140001e40)
// WARNING: Removing unreachable block (ram,0x000140001e48)
// WARNING: Removing unreachable block (ram,0x000140001e56)
// WARNING: Removing unreachable block (ram,0x000140001f60)
// WARNING: Removing unreachable block (ram,0x000140001dd2)
// WARNING: Removing unreachable block (ram,0x000140001fb0)
// WARNING: Removing unreachable block (ram,0x000140001fb9)
// WARNING: Removing unreachable block (ram,0x000140001fc0)
// WARNING: Removing unreachable block (ram,0x000140001fdd)
// WARNING: Removing unreachable block (ram,0x000140001eb0)
// WARNING: Removing unreachable block (ram,0x000140001ebe)
// WARNING: Removing unreachable block (ram,0x000140001ed0)
// WARNING: Removing unreachable block (ram,0x000140001ee2)
// WARNING: Removing unreachable block (ram,0x000140001eef)
// WARNING: Removing unreachable block (ram,0x000140001f00)
// WARNING: Enum "SectionFlags": Some values do not have unique names

void FUN_140001b30(uint *param_1, undefined8 param_2, undefined8 param_3,
                   undefined8 param_4)

{
  BOOL BVar1;
  DWORD DVar2;
  ulonglong *puVar3;
  IMAGE_SECTION_HEADER *pIVar4;
  undefined4 *puVar5;
  IMAGE_DOS_HEADER *pIVar6;
  SIZE_T SVar7;
  ulonglong uVar8;
  longlong lVar9;
  uint *in_R8;
  uint uVar10;
  PDWORD in_R9;
  undefined1 auStack_c0[24];
  uint *puStack_a8;
  longlong lStack_a0;
  IMAGE_SECTION_HEADER *pIStack_98;
  _MEMORY_BASIC_INFORMATION local_48;

  lVar9 = (longlong)(int)DAT_14000e0a4;
  if ((int)DAT_14000e0a4 < 1)
    goto LAB_140001c60;
  in_R9 = (PDWORD)0x0;
  puVar3 = (ulonglong *)(DAT_14000e0a8 + 0x18);
  do {
    in_R8 = (uint *)*puVar3;
    if ((in_R8 <= param_1) &&
        (in_R8 =
             (uint *)((longlong)in_R8 + (ulonglong) * (uint *)(puVar3[1] + 8)),
         param_1 < in_R8)) {
      return;
    }
    uVar10 = (int)in_R9 + 1;
    in_R9 = (PDWORD)(ulonglong)uVar10;
    puVar3 = puVar3 + 5;
  } while (uVar10 != DAT_14000e0a4);
  do {
    pIVar4 = FUN_1400025a0((longlong)param_1);
    if (pIVar4 == (IMAGE_SECTION_HEADER *)0x0) {
    LAB_140001c82:
      FUN_140001ac0("Address %p has no image-section", param_1, in_R8, in_R9);
      if (DAT_14000e0a0 == 0) {
        DAT_14000e0a0 = 1;
        puStack_a8 = param_1;
        lStack_a0 = lVar9;
        pIStack_98 = pIVar4;
        FUN_140002620();
        uVar8 = FUN_140002880();
        DAT_14000e0a4 = 0;
        DAT_14000e0a8 = auStack_c0 + -uVar8;
      }
      return;
    }
    param_1 = (uint *)(lVar9 * 0x28);
    puVar5 = (undefined4 *)(DAT_14000e0a8 + (longlong)param_1);
    *(IMAGE_SECTION_HEADER **)(puVar5 + 8) = pIVar4;
    *puVar5 = 0;
    pIVar6 = FUN_1400026e0();
    uVar10 = pIVar4->VirtualAddress;
    *(char **)(DAT_14000e0a8 + 0x18 + (longlong)param_1) =
        pIVar6->e_magic + uVar10;
    SVar7 = VirtualQuery(pIVar6->e_magic + uVar10, &local_48, 0x30);
    if (SVar7 == 0) {
      in_R8 = *(uint **)(DAT_14000e0a8 + 0x18 + (longlong)param_1);
      FUN_140001ac0("  VirtualQuery failed for %d bytes at address %p",
                    (ulonglong)(pIVar4->Misc).PhysicalAddress, in_R8, in_R9);
      goto LAB_140001c82;
    }
    if (((local_48.Protect - 4 & 0xfffffffb) == 0) ||
        ((local_48.Protect - 0x40 & 0xffffffbf) == 0)) {
    LAB_140001bfe:
      DAT_14000e0a4 = DAT_14000e0a4 + 1;
      return;
    }
    in_R8 = (uint *)0x40;
    if (local_48.Protect == 2) {
      in_R8 = (uint *)0x4;
    }
    param_1 = (uint *)((longlong)param_1 + (longlong)DAT_14000e0a8);
    *(PVOID *)(param_1 + 2) = local_48.BaseAddress;
    *(SIZE_T *)(param_1 + 4) = local_48.RegionSize;
    in_R9 = param_1;
    BVar1 = VirtualProtect(local_48.BaseAddress, local_48.RegionSize,
                           (DWORD)in_R8, param_1);
    if (BVar1 != 0)
      goto LAB_140001bfe;
    DVar2 = GetLastError();
    FUN_140001ac0("  VirtualProtect failed with code 0x%x", (ulonglong)DVar2,
                  in_R8, in_R9);
  LAB_140001c60:
    lVar9 = 0;
  } while (true);
}

// WARNING: Removing unreachable block (ram,0x000140001d31)
// WARNING: Removing unreachable block (ram,0x000140001d3d)
// WARNING: Removing unreachable block (ram,0x000140001d47)
// WARNING: Removing unreachable block (ram,0x000140001d4a)
// WARNING: Removing unreachable block (ram,0x000140001d52)
// WARNING: Removing unreachable block (ram,0x000140001d5e)
// WARNING: Removing unreachable block (ram,0x000140001d6b)
// WARNING: Removing unreachable block (ram,0x000140001ddf)
// WARNING: Removing unreachable block (ram,0x000140001f08)
// WARNING: Removing unreachable block (ram,0x000140001f88)
// WARNING: Removing unreachable block (ram,0x000140001f92)
// WARNING: Removing unreachable block (ram,0x000140001f14)
// WARNING: Removing unreachable block (ram,0x000140001f2b)
// WARNING: Removing unreachable block (ram,0x000140001f34)
// WARNING: Removing unreachable block (ram,0x000140001f47)
// WARNING: Removing unreachable block (ram,0x000140001dfc)
// WARNING: Removing unreachable block (ram,0x000140001d80)
// WARNING: Removing unreachable block (ram,0x000140001d89)
// WARNING: Removing unreachable block (ram,0x000140001d92)
// WARNING: Removing unreachable block (ram,0x000140001f70)
// WARNING: Removing unreachable block (ram,0x000140001f7e)
// WARNING: Removing unreachable block (ram,0x000140001da4)
// WARNING: Removing unreachable block (ram,0x000140001db5)
// WARNING: Removing unreachable block (ram,0x000140001dbe)
// WARNING: Removing unreachable block (ram,0x000140001dc7)
// WARNING: Removing unreachable block (ram,0x000140001e60)
// WARNING: Removing unreachable block (ram,0x000140001f98)
// WARNING: Removing unreachable block (ram,0x000140001fa6)
// WARNING: Removing unreachable block (ram,0x000140001e72)
// WARNING: Removing unreachable block (ram,0x000140001e83)
// WARNING: Removing unreachable block (ram,0x000140001e8c)
// WARNING: Removing unreachable block (ram,0x000140001e92)
// WARNING: Removing unreachable block (ram,0x000140001eaa)
// WARNING: Removing unreachable block (ram,0x000140001dfe)
// WARNING: Removing unreachable block (ram,0x000140001fe2)
// WARNING: Removing unreachable block (ram,0x000140001ff0)
// WARNING: Removing unreachable block (ram,0x000140002014)
// WARNING: Removing unreachable block (ram,0x000140002039)
// WARNING: Removing unreachable block (ram,0x000140001e07)
// WARNING: Removing unreachable block (ram,0x000140001e1e)
// WARNING: Removing unreachable block (ram,0x000140001e23)
// WARNING: Removing unreachable block (ram,0x000140001e40)
// WARNING: Removing unreachable block (ram,0x000140001e48)
// WARNING: Removing unreachable block (ram,0x000140001e56)
// WARNING: Removing unreachable block (ram,0x000140001f60)
// WARNING: Removing unreachable block (ram,0x000140001dd2)
// WARNING: Removing unreachable block (ram,0x000140001fb0)
// WARNING: Removing unreachable block (ram,0x000140001fb9)
// WARNING: Removing unreachable block (ram,0x000140001fc0)
// WARNING: Removing unreachable block (ram,0x000140001fdd)
// WARNING: Removing unreachable block (ram,0x000140001eb0)
// WARNING: Removing unreachable block (ram,0x000140001ebe)
// WARNING: Removing unreachable block (ram,0x000140001ed0)
// WARNING: Removing unreachable block (ram,0x000140001ee2)
// WARNING: Removing unreachable block (ram,0x000140001eef)
// WARNING: Removing unreachable block (ram,0x000140001f00)

void FUN_140001ca0(undefined8 param_1, undefined8 param_2, undefined8 param_3,
                   undefined8 param_4)

{
  ulonglong uVar1;
  undefined1 auStack_58[24];

  if (DAT_14000e0a0 == 0) {
    DAT_14000e0a0 = 1;
    FUN_140002620();
    uVar1 = FUN_140002880();
    DAT_14000e0a4 = 0;
    DAT_14000e0a8 = auStack_58 + -uVar1;
  }
  return;
}

void FUN_140002040(undefined8 param_1)

{
  DAT_14000e0b0 = param_1;
  __setusermatherr();
  return;
}

void FUN_140002210(void)

{
  DWORD *pDVar1;
  DWORD DVar2;
  LPVOID pvVar3;

  EnterCriticalSection((LPCRITICAL_SECTION)&DAT_14000e100);
  for (pDVar1 = DAT_14000e0e0; pDVar1 != (DWORD *)0x0;
       pDVar1 = *(DWORD **)(pDVar1 + 4)) {
    pvVar3 = TlsGetValue(*pDVar1);
    DVar2 = GetLastError();
    if ((pvVar3 != (LPVOID)0x0) && (DVar2 == 0)) {
      (**(code **)(pDVar1 + 2))(pvVar3);
    }
  }
  // WARNING: Could not recover jumptable at 0x000140002279. Too many branches
  // WARNING: Treating indirect jump as call
  LeaveCriticalSection((LPCRITICAL_SECTION)&DAT_14000e100);
  return;
}

undefined8 FUN_140002380(undefined8 param_1, uint param_2)

{
  void *pvVar1;
  void *_Memory;

  if (param_2 == 2) {
    FUN_140001ab0();
    return 1;
  }
  if (param_2 < 3) {
    if (param_2 == 0) {
      if (DAT_14000e0e8 != 0) {
        FUN_140002210();
      }
      if (DAT_14000e0e8 == 1) {
        DAT_14000e0e8 = 1;
        _Memory = DAT_14000e0e0;
        while (_Memory != (void *)0x0) {
          pvVar1 = *(void **)((longlong)_Memory + 0x10);
          free(_Memory);
          _Memory = pvVar1;
        }
        DAT_14000e0e0 = (void *)0x0;
        DAT_14000e0e8 = 0;
        DeleteCriticalSection((LPCRITICAL_SECTION)&DAT_14000e100);
      }
    } else {
      if (DAT_14000e0e8 == 0) {
        InitializeCriticalSection((LPCRITICAL_SECTION)&DAT_14000e100);
      }
      DAT_14000e0e8 = 1;
    }
  } else if ((param_2 == 3) && (DAT_14000e0e8 != 0)) {
    FUN_140002210();
  }
  return 1;
}

// WARNING: Enum "SectionFlags": Some values do not have unique names

IMAGE_SECTION_HEADER *FUN_1400025a0(longlong param_1)

{
  IMAGE_SECTION_HEADER *pIVar1;

  pIVar1 = &IMAGE_SECTION_HEADER_140000188;
  while (
      (param_1 - 0x140000000U < (ulonglong)(uint)pIVar1->VirtualAddress ||
       ((ulonglong)(pIVar1->VirtualAddress + (pIVar1->Misc).PhysicalAddress) <=
        param_1 - 0x140000000U))) {
    pIVar1 = pIVar1 + 1;
    if (pIVar1 == (IMAGE_SECTION_HEADER *)&DAT_1400004a8) {
      return (IMAGE_SECTION_HEADER *)0x0;
    }
  }
  return pIVar1;
}

// WARNING: Removing unreachable block (ram,0x00014000263f)

word FUN_140002620(void)

{
  return 0x14;
}

// WARNING: Removing unreachable block (ram,0x0001400026ff)

IMAGE_DOS_HEADER *FUN_1400026e0(void)

{
  return &IMAGE_DOS_HEADER_140000000;
}

ulonglong FUN_140002880(void)

{
  ulonglong in_RAX;
  ulonglong uVar1;
  undefined8 *puVar2;
  undefined8 local_res8[4];

  puVar2 = local_res8;
  uVar1 = in_RAX;
  if (0xfff < in_RAX) {
    do {
      puVar2 = puVar2 + -0x200;
      *puVar2 = *puVar2;
      uVar1 = uVar1 - 0x1000;
    } while (0x1000 < uVar1);
  }
  *(undefined8 *)((longlong)puVar2 - uVar1) =
      *(undefined8 *)((longlong)puVar2 - uVar1);
  return in_RAX;
}

uint FUN_1400028c0(FILE *param_1, char *param_2, ulonglong *param_3)

{
  uint uVar1;

  FUN_1400077f0(param_1);
  uVar1 = FUN_1400044d0(0x6000, param_1, 0, param_2, param_3);
  FUN_140007860(param_1);
  return uVar1;
}

void FUN_140002910(uint param_1, ulonglong *param_2, uint param_3,
                   uint *param_4, uint *param_5)

{
  uint uVar1;
  int iVar2;
  ushort uVar3;
  uint local_24;
  undefined8 local_20;
  ulonglong local_18;
  uint local_10;

  local_18 = *param_2;
  local_10 = (uint)param_2[1];
  uVar3 = (ushort)local_10 & 0x7fff;
  if ((local_10 & 0x7fff) == 0) {
    if ((int)local_18 == 0 && (int)(local_18 >> 0x20) == 0) {
      local_24 = 0;
      iVar2 = 0;
    } else {
      if ((longlong)local_18 < 0)
        goto LAB_14000294b;
      local_24 = 2;
      iVar2 = -0x403d;
    }
  } else if (uVar3 == 0x7fff) {
    if ((local_18 & 0x7fffffff00000000) != 0 || (int)local_18 != 0) {
      local_24 = 4;
      iVar2 = 0;
      uVar1 = 0;
      goto LAB_140002964;
    }
    local_24 = 3;
    iVar2 = 0;
  } else {
  LAB_14000294b:
    local_24 = 1;
    iVar2 = (int)(short)(uVar3 + 0xbfc2);
  }
  uVar1 = local_10 & 0x8000;
LAB_140002964:
  *param_5 = uVar1;
  FUN_140005210((int *)&DAT_140009040, iVar2, (uint *)&local_18, &local_24,
                param_1, param_3, param_4, &local_20);
  return;
}

void FUN_140002a00(int param_1, undefined8 *param_2)

{
  int iVar1;

  if (((*(uint *)(param_2 + 1) & 0x4000) != 0) ||
      (iVar1 = *(int *)((longlong)param_2 + 0x24),
       iVar1 < *(int *)(param_2 + 5))) {
    if ((*(uint *)(param_2 + 1) & 0x2000) != 0) {
      fputc(param_1, (FILE *)*param_2);
      *(int *)((longlong)param_2 + 0x24) =
          *(int *)((longlong)param_2 + 0x24) + 1;
      return;
    }
    *(char *)((longlong) & ((FILE *)*param_2)->_ptr +
                               (longlong) * (int *)((longlong)param_2 + 0x24)) =
        (char)param_1;
    iVar1 = *(int *)((longlong)param_2 + 0x24);
  }
  *(int *)((longlong)param_2 + 0x24) = iVar1 + 1;
  return;
}

void FUN_140002a60(longlong param_1, int param_2, undefined8 *param_3)

{
  int iVar1;
  longlong lVar2;
  int iVar3;
  longlong lVar4;
  LPSTR pCVar5;
  LPSTR pCVar6;
  CHAR local_58[24];

  FUN_140007990(local_58, L'\0');
  iVar1 = *(int *)(param_3 + 2);
  iVar3 = iVar1;
  if (param_2 <= iVar1) {
    iVar3 = param_2;
  }
  if (-1 < iVar1) {
    param_2 = iVar3;
  }
  if (param_2 < *(int *)((longlong)param_3 + 0xc)) {
    iVar1 = *(int *)((longlong)param_3 + 0xc) - param_2;
    *(int *)((longlong)param_3 + 0xc) = iVar1;
    if ((*(byte *)((longlong)param_3 + 9) & 4) == 0) {
      *(int *)((longlong)param_3 + 0xc) = iVar1 + -1;
      do {
        FUN_140002a00(0x20, param_3);
        iVar1 = *(int *)((longlong)param_3 + 0xc);
        *(int *)((longlong)param_3 + 0xc) = iVar1 + -1;
      } while (iVar1 != 0);
      if (param_2 < 1)
        goto LAB_140002b6d;
    } else if (param_2 < 1) {
      *(int *)((longlong)param_3 + 0xc) =
          *(int *)((longlong)param_3 + 0xc) + -1;
      goto LAB_140002b60;
    }
  } else {
    *(undefined4 *)((longlong)param_3 + 0xc) = 0xffffffff;
    if (param_2 < 1) {
      *(undefined4 *)((longlong)param_3 + 0xc) = 0xfffffffe;
      return;
    }
  }
  lVar4 = 0;
  do {
    lVar2 = FUN_140007990(local_58, *(WCHAR *)(param_1 + lVar4 * 2));
    if ((int)lVar2 < 1)
      goto LAB_140002b6d;
    pCVar5 = local_58;
    do {
      while (true) {
        pCVar6 = pCVar5 + 1;
        if (((*(uint *)(param_3 + 1) & 0x4000) != 0) ||
            (iVar1 = *(int *)((longlong)param_3 + 0x24),
             iVar1 < *(int *)(param_3 + 5)))
          break;
      LAB_140002afa:
        *(int *)((longlong)param_3 + 0x24) = iVar1 + 1;
        pCVar5 = pCVar6;
        if (pCVar6 == local_58 + (ulonglong)((int)lVar2 - 1) + 1)
          goto LAB_140002b3c;
      }
      if ((*(uint *)(param_3 + 1) & 0x2000) == 0) {
        *(CHAR *)((longlong) &
                  ((FILE *)*param_3)->_ptr +
                      (longlong) * (int *)((longlong)param_3 + 0x24)) = *pCVar5;
        iVar1 = *(int *)((longlong)param_3 + 0x24);
        goto LAB_140002afa;
      }
      fputc((int)*pCVar5, (FILE *)*param_3);
      *(int *)((longlong)param_3 + 0x24) =
          *(int *)((longlong)param_3 + 0x24) + 1;
      pCVar5 = pCVar6;
    } while (pCVar6 != local_58 + (ulonglong)((int)lVar2 - 1) + 1);
  LAB_140002b3c:
    lVar4 = lVar4 + 1;
  } while (0 < param_2 - (int)lVar4);
  iVar1 = *(int *)((longlong)param_3 + 0xc);
  *(int *)((longlong)param_3 + 0xc) = iVar1 + -1;
  if (iVar1 < 1) {
    return;
  }
LAB_140002b60:
  do {
    FUN_140002a00(0x20, param_3);
  LAB_140002b6d:
    iVar1 = *(int *)((longlong)param_3 + 0xc);
    *(int *)((longlong)param_3 + 0xc) = iVar1 + -1;
  } while (0 < iVar1);
  return;
}

void FUN_140002bf0(char *param_1, uint param_2, undefined8 *param_3)

{
  uint uVar1;
  int iVar2;
  uint uVar3;
  char *pcVar4;

  uVar1 = *(uint *)(param_3 + 2);
  uVar3 = uVar1;
  if ((int)param_2 <= (int)uVar1) {
    uVar3 = param_2;
  }
  if (-1 < (int)uVar1) {
    param_2 = uVar3;
  }
  if ((int)param_2 < *(int *)((longlong)param_3 + 0xc)) {
    iVar2 = *(int *)((longlong)param_3 + 0xc) - param_2;
    *(int *)((longlong)param_3 + 0xc) = iVar2;
    uVar1 = *(uint *)(param_3 + 1);
    if ((uVar1 & 0x400) == 0) {
      *(int *)((longlong)param_3 + 0xc) = iVar2 + -1;
      do {
        FUN_140002a00(0x20, param_3);
        iVar2 = *(int *)((longlong)param_3 + 0xc);
        *(int *)((longlong)param_3 + 0xc) = iVar2 + -1;
      } while (iVar2 != 0);
      if (param_2 == 0)
        goto LAB_140002c91;
      goto LAB_140002c2e;
    }
    if (param_2 == 0) {
      *(int *)((longlong)param_3 + 0xc) =
          *(int *)((longlong)param_3 + 0xc) + -1;
      goto LAB_140002ca1;
    }
  } else {
    *(undefined4 *)((longlong)param_3 + 0xc) = 0xffffffff;
    if (param_2 == 0) {
      *(undefined4 *)((longlong)param_3 + 0xc) = 0xfffffffe;
      return;
    }
  LAB_140002c2e:
    uVar1 = *(uint *)(param_3 + 1);
  }
  pcVar4 = param_1;
  while (true) {
    if (((uVar1 & 0x4000) != 0) || (iVar2 = *(int *)((longlong)param_3 + 0x24),
                                    iVar2 < *(int *)(param_3 + 5))) {
      if ((uVar1 & 0x2000) == 0) {
        *(char *)((longlong) &
                  ((FILE *)*param_3)->_ptr +
                      (longlong) * (int *)((longlong)param_3 + 0x24)) = *pcVar4;
        iVar2 = *(int *)((longlong)param_3 + 0x24);
      } else {
        fputc((int)*pcVar4, (FILE *)*param_3);
        iVar2 = *(int *)((longlong)param_3 + 0x24);
      }
    }
    *(int *)((longlong)param_3 + 0x24) = iVar2 + 1;
    if (pcVar4 + 1 == param_1 + param_2)
      break;
    uVar1 = *(uint *)(param_3 + 1);
    pcVar4 = pcVar4 + 1;
  }
LAB_140002c91:
  while (iVar2 = *(int *)((longlong)param_3 + 0xc),
         *(int *)((longlong)param_3 + 0xc) = iVar2 + -1, 0 < iVar2) {
    uVar1 = *(uint *)(param_3 + 1);
  LAB_140002ca1:
    if (((uVar1 & 0x4000) != 0) || (iVar2 = *(int *)((longlong)param_3 + 0x24),
                                    iVar2 < *(int *)(param_3 + 5))) {
      if ((uVar1 & 0x2000) == 0) {
        *(undefined1 *)((longlong) &
                        ((FILE *)*param_3)->_ptr +
                            (longlong) * (int *)((longlong)param_3 + 0x24)) =
            0x20;
        iVar2 = *(int *)((longlong)param_3 + 0x24);
      } else {
        fputc(0x20, (FILE *)*param_3);
        iVar2 = *(int *)((longlong)param_3 + 0x24);
      }
    }
    *(int *)((longlong)param_3 + 0x24) = iVar2 + 1;
  }
  return;
}

void FUN_140002d40(char *param_1, undefined8 *param_2)

{
  uint uVar1;
  size_t sVar3;
  ulonglong uVar2;

  if (param_1 == (char *)0x0) {
    param_1 = "(null)";
  }
  if (*(int *)(param_2 + 2) < 0) {
    sVar3 = strlen(param_1);
    uVar1 = (uint)sVar3;
  } else {
    uVar2 = FUN_140007770(param_1, (longlong) * (int *)(param_2 + 2));
    uVar1 = (uint)uVar2;
  }
  FUN_140002bf0(param_1, uVar1, param_2);
  return;
}

void FUN_140002d90(int param_1, longlong param_2, undefined8 *param_3)

{
  uint uVar1;
  byte bVar2;
  longlong lVar3;
  byte *pbVar4;
  byte local_c[12];

  uVar1 = *(uint *)(param_3 + 1);
  *(undefined4 *)(param_3 + 2) = 0xffffffff;
  if (param_1 == 0) {
    bVar2 = 0x2b;
    if ((uVar1 & 0x100) == 0) {
      if ((uVar1 & 0x40) == 0) {
        pbVar4 = local_c;
      } else {
        pbVar4 = local_c + 1;
        local_c[0] = 0x20;
      }
      goto LAB_140002dcb;
    }
  } else {
    bVar2 = 0x2d;
  }
  pbVar4 = local_c + 1;
  local_c[0] = bVar2;
LAB_140002dcb:
  lVar3 = 0;
  do {
    pbVar4[lVar3] = *(byte *)(param_2 + lVar3) & 0xdf | (byte)uVar1 & 0x20;
    lVar3 = lVar3 + 1;
  } while (lVar3 != 3);
  FUN_140002bf0((char *)local_c, ((int)pbVar4 + 3) - (int)local_c, param_3);
  return;
}

void FUN_140002e30(int param_1, ulonglong param_2, undefined8 *param_3)

{
  FILE *pFVar1;
  longlong lVar2;
  int iVar3;
  int iVar4;
  byte bVar5;
  int iVar6;
  int iVar7;
  ulonglong uVar8;
  byte bVar9;
  undefined1 *puVar10;
  undefined1 *puVar11;
  byte *pbVar12;
  byte *pbVar13;
  byte *pbVar14;
  uint uVar15;
  byte bVar16;
  byte *pbVar17;
  byte bVar18;
  int iVar19;
  byte bVar20;
  bool bVar21;
  undefined1 auStack_78[32];
  byte abStack_58[12];
  int local_4c;

  bVar18 = (byte)param_1;
  if (param_1 == 0x6f) {
    iVar19 = *(int *)(param_3 + 2);
    uVar15 = *(uint *)(param_3 + 1);
    if ((uVar15 & 0x1000) == 0) {
      local_4c = *(int *)((longlong)param_3 + 0xc);
      uVar8 = FUN_140002880();
      bVar9 = 3;
      bVar16 = 7;
      puVar11 = auStack_78 + -uVar8;
      pbVar17 = abStack_58 + -uVar8;
      goto LAB_140002f85;
    }
    bVar9 = 3;
  LAB_140002e79:
    local_4c = *(int *)((longlong)param_3 + 0xc);
    uVar8 = FUN_140002880();
    lVar2 = -uVar8;
    puVar11 = auStack_78 + lVar2;
    puVar10 = auStack_78 + lVar2;
    pbVar17 = abStack_58 + lVar2;
    bVar16 = (param_1 != 0x6f) * '\b' + 7;
    pbVar12 = pbVar17;
    if (param_2 == 0)
      goto LAB_140002ed8;
  LAB_140002f8e:
    pbVar14 = pbVar17;
    do {
      pbVar13 = pbVar14;
      pbVar14 = pbVar13 + 1;
      bVar5 = bVar16 & (byte)param_2;
      bVar20 = bVar5 + 0x30;
      bVar5 = bVar5 + 0x37 | bVar18 & 0x20;
      if (bVar20 < 0x3a) {
        bVar5 = bVar20;
      }
      param_2 = param_2 >> (bVar9 & 0x3f);
      *pbVar13 = bVar5;
    } while (param_2 != 0);
    puVar10 = puVar11;
    pbVar12 = pbVar17;
    if (pbVar14 == pbVar17)
      goto LAB_140002ed8;
    iVar7 = (int)pbVar14;
    iVar3 = (int)pbVar17;
    if (0 < iVar19) {
      iVar6 = iVar7 - iVar3;
      iVar4 = iVar19 - iVar6;
      if (iVar19 - iVar6 < 1) {
        if (param_1 != 0x6f) {
          if (local_4c <= iVar6)
            goto LAB_1400032a0;
          iVar6 = local_4c - iVar6;
          *(int *)((longlong)param_3 + 0xc) = iVar6;
          goto LAB_140003010;
        }
        goto LAB_140003238;
      }
      goto LAB_140002ef1;
    }
    if (param_1 == 0x6f) {
    LAB_140003238:
      if ((uVar15 & 0x800) != 0) {
        *pbVar14 = 0x30;
        pbVar12 = pbVar13 + 2;
        goto LAB_140002f0a;
      }
      iVar6 = iVar7 - iVar3;
      if (iVar6 < local_4c)
        goto LAB_1400031e4;
      *(undefined4 *)((longlong)param_3 + 0xc) = 0xffffffff;
      pbVar12 = pbVar14;
      goto LAB_140002f37;
    }
    if (iVar7 - iVar3 < local_4c) {
      iVar6 = local_4c - (iVar7 - iVar3);
      *(int *)((longlong)param_3 + 0xc) = iVar6;
      goto LAB_140003010;
    }
  LAB_1400032a0:
    *(undefined4 *)((longlong)param_3 + 0xc) = 0xffffffff;
  LAB_1400032a7:
    iVar6 = -1;
    pbVar12 = pbVar14;
    if ((uVar15 & 0x800) != 0) {
      *pbVar14 = bVar18;
      iVar6 = -1;
      pbVar14[1] = 0x30;
      pbVar12 = pbVar14 + 2;
    }
  } else {
    iVar19 = *(int *)(param_3 + 2);
    uVar15 = *(uint *)(param_3 + 1);
    if ((uVar15 & 0x1000) != 0) {
      bVar9 = 4;
      goto LAB_140002e79;
    }
    local_4c = *(int *)((longlong)param_3 + 0xc);
    uVar8 = FUN_140002880();
    bVar9 = 4;
    bVar16 = 0xf;
    puVar11 = auStack_78 + -uVar8;
    pbVar17 = abStack_58 + -uVar8;
  LAB_140002f85:
    puVar10 = puVar11;
    pbVar12 = pbVar17;
    if (param_2 != 0)
      goto LAB_140002f8e;
  LAB_140002ed8:
    *(uint *)(param_3 + 1) = uVar15 & 0xfffff7ff;
    pbVar14 = pbVar12;
    pbVar17 = pbVar12;
    iVar4 = iVar19;
    if (iVar19 < 1) {
    LAB_1400031bb:
      iVar7 = local_4c;
      pbVar14 = pbVar12;
      if (iVar19 == 0)
        goto LAB_140002f13;
      pbVar14 = pbVar12 + 1;
      *pbVar12 = 0x30;
      iVar6 = (int)pbVar14 - (int)pbVar17;
      if (iVar6 < iVar7)
        goto LAB_1400031e1;
    LAB_140002f26:
      *(undefined4 *)((longlong)param_3 + 0xc) = 0xffffffff;
      puVar11 = puVar10;
      pbVar12 = pbVar14;
      if (param_1 == 0x6f) {
      LAB_140002f37:
        if (pbVar12 <= pbVar17) {
          return;
        }
        uVar15 = *(uint *)(param_3 + 1);
        iVar19 = -2;
        iVar6 = -1;
        goto LAB_140003080;
      }
      uVar15 = *(uint *)(param_3 + 1);
      goto LAB_1400032a7;
    }
  LAB_140002ef1:
    pbVar12 = pbVar14 + iVar4;
    *(undefined8 *)(puVar10 + -8) = 0x140002f0a;
    memset(pbVar14, 0x30, (longlong)iVar4);
  LAB_140002f0a:
    pbVar14 = pbVar12;
    if (pbVar12 == pbVar17)
      goto LAB_1400031bb;
  LAB_140002f13:
    iVar6 = (int)pbVar14 - (int)pbVar17;
    if (local_4c <= iVar6)
      goto LAB_140002f26;
  LAB_1400031e1:
    uVar15 = *(uint *)(param_3 + 1);
    puVar11 = puVar10;
  LAB_1400031e4:
    iVar6 = local_4c - iVar6;
    *(int *)((longlong)param_3 + 0xc) = iVar6;
    if (param_1 == 0x6f) {
      pbVar12 = pbVar14;
      if ((-1 < iVar19) || ((uVar15 & 0x600) != 0x200))
        goto LAB_140003025;
      *(undefined8 *)(puVar11 + -8) = 0x140003227;
      memset(pbVar14, 0x30, (longlong)iVar6);
      pbVar14 = pbVar14 + iVar6;
    LAB_14000322b:
      iVar6 = -1;
      pbVar12 = pbVar14;
    } else {
    LAB_140003010:
      if ((uVar15 & 0x800) == 0) {
        pbVar12 = pbVar14;
        if ((-1 < iVar19) || ((uVar15 & 0x600) != 0x200)) {
        LAB_140003025:
          iVar19 = iVar6 + -1;
          if ((uVar15 & 0x400) == 0) {
            do {
              *(undefined8 *)(puVar11 + -8) = 0x14000304d;
              FUN_140002a00(0x20, param_3);
              bVar21 = iVar19 != 0;
              iVar6 = iVar19 + -1;
              iVar19 = iVar6;
            } while (bVar21);
            iVar19 = -2;
            if (pbVar17 < pbVar12)
              goto LAB_14000307d;
            return;
          }
          if (pbVar12 <= pbVar17)
            goto LAB_1400030da;
          goto LAB_140003080;
        }
      LAB_1400032fb:
        *(undefined8 *)(puVar11 + -8) = 0x14000330e;
        memset(pbVar14, 0x30, (longlong)iVar6);
        pbVar14 = pbVar14 + iVar6;
        if ((uVar15 & 0x800) == 0)
          goto LAB_14000322b;
        *pbVar14 = bVar18;
        iVar6 = -1;
        pbVar12 = pbVar14 + 2;
        pbVar14[1] = 0x30;
      } else {
        iVar6 = iVar6 + -2;
        if (0 < iVar6) {
          if ((iVar19 < 0) && ((uVar15 & 0x600) == 0x200))
            goto LAB_1400032fb;
          *pbVar14 = bVar18;
          pbVar12 = pbVar14 + 2;
          pbVar14[1] = 0x30;
          goto LAB_140003025;
        }
        *pbVar14 = bVar18;
        pbVar12 = pbVar14 + 2;
        pbVar14[1] = 0x30;
      }
    }
  }
  if (pbVar12 <= pbVar17) {
    return;
  }
  uVar15 = *(uint *)(param_3 + 1);
  iVar19 = iVar6 + -1;
LAB_140003080:
  do {
    pbVar12 = pbVar12 + -1;
    if (((uVar15 & 0x4000) == 0) && (iVar7 = *(int *)((longlong)param_3 + 0x24),
                                     *(int *)(param_3 + 5) <= iVar7)) {
    LAB_140003072:
      *(int *)((longlong)param_3 + 0x24) = iVar7 + 1;
    } else {
      bVar18 = *pbVar12;
      pFVar1 = (FILE *)*param_3;
      if ((uVar15 & 0x2000) == 0) {
        *(byte *)((longlong)&pFVar1->_ptr +
                  (longlong) * (int *)((longlong)param_3 + 0x24)) = bVar18;
        iVar7 = *(int *)((longlong)param_3 + 0x24);
        goto LAB_140003072;
      }
      *(undefined8 *)(puVar11 + -8) = 0x1400030a7;
      fputc((int)(char)bVar18, pFVar1);
      *(int *)((longlong)param_3 + 0x24) =
          *(int *)((longlong)param_3 + 0x24) + 1;
    }
    if (pbVar12 <= pbVar17)
      break;
  LAB_14000307d:
    uVar15 = *(uint *)(param_3 + 1);
  } while (true);
  if (iVar6 < 1) {
    return;
  }
  do {
    while (true) {
      uVar15 = *(uint *)(param_3 + 1);
    LAB_1400030da:
      if (((uVar15 & 0x4000) != 0) ||
          (iVar7 = *(int *)((longlong)param_3 + 0x24),
           iVar7 < *(int *)(param_3 + 5)))
        break;
    LAB_1400030cb:
      *(int *)((longlong)param_3 + 0x24) = iVar7 + 1;
      bVar21 = iVar19 == 0;
      iVar19 = iVar19 + -1;
      if (bVar21) {
        return;
      }
    }
    pFVar1 = (FILE *)*param_3;
    if ((uVar15 & 0x2000) == 0) {
      *(undefined1 *)((longlong)&pFVar1->_ptr +
                      (longlong) * (int *)((longlong)param_3 + 0x24)) = 0x20;
      iVar7 = *(int *)((longlong)param_3 + 0x24);
      goto LAB_1400030cb;
    }
    *(undefined8 *)(puVar11 + -8) = 0x1400030ff;
    fputc(0x20, pFVar1);
    *(int *)((longlong)param_3 + 0x24) = *(int *)((longlong)param_3 + 0x24) + 1;
    bVar21 = iVar19 == 0;
    iVar19 = iVar19 + -1;
    if (bVar21) {
      return;
    }
  } while (true);
}

void FUN_140003360(ulonglong param_1, undefined8 *param_2)

{
  char *pcVar1;
  char cVar2;
  FILE *pFVar3;
  longlong lVar4;
  int iVar5;
  ulonglong uVar6;
  int iVar7;
  uint uVar8;
  int iVar9;
  char *pcVar10;
  char *_Dst;
  bool bVar11;
  undefined8 auStack_70[5];
  char local_48[8];

  iVar5 = *(int *)(param_2 + 2);
  uVar8 = *(uint *)(param_2 + 1);
  iVar7 = *(int *)((longlong)param_2 + 0xc);
  auStack_70[0] = 0x1400033b5;
  uVar6 = FUN_140002880();
  lVar4 = -uVar6;
  pcVar1 = local_48 + lVar4;
  if ((uVar8 & 0x80) == 0) {
  LAB_1400033d3:
    if (param_1 != 0)
      goto LAB_1400033dc;
    bVar11 = true;
    pcVar10 = pcVar1;
    _Dst = pcVar1;
    iVar9 = iVar5;
    if (0 < iVar5)
      goto LAB_14000347a;
  LAB_140003496:
    if ((iVar5 == 0) || (pcVar10 = _Dst, !bVar11))
      goto LAB_1400034a3;
  } else {
    if (-1 < (longlong)param_1) {
      uVar8 = uVar8 & 0xffffff7f;
      *(uint *)(param_2 + 1) = uVar8;
      goto LAB_1400033d3;
    }
    param_1 = -param_1;
  LAB_1400033dc:
    pcVar10 = pcVar1;
    do {
      if ((((pcVar1 != pcVar10) && ((uVar8 & 0x1000) != 0)) &&
           (*(short *)(param_2 + 4) != 0)) &&
          (((longlong)pcVar10 - (longlong)pcVar1 & 0x8000000000000003U) == 3)) {
        *pcVar10 = ',';
        pcVar10 = pcVar10 + 1;
      }
      _Dst = pcVar10 + 1;
      *pcVar10 = (char)param_1 + (char)(param_1 / 10) * -10 + '0';
      bVar11 = 9 < param_1;
      param_1 = param_1 / 10;
      pcVar10 = _Dst;
    } while (bVar11);
    if (iVar5 < 1) {
    LAB_140003490:
      bVar11 = pcVar1 == _Dst;
      goto LAB_140003496;
    }
    iVar9 = iVar5 - ((int)_Dst - (int)pcVar1);
    if (0 < iVar9) {
    LAB_14000347a:
      _Dst = pcVar10 + iVar9;
      *(undefined8 *)((longlong)auStack_70 + lVar4) = 0x140003490;
      memset(pcVar10, 0x30, (longlong)iVar9);
      goto LAB_140003490;
    }
    pcVar10 = pcVar1;
    if (pcVar1 != _Dst)
      goto LAB_1400034a3;
  }
  *pcVar10 = '0';
  _Dst = pcVar10 + 1;
LAB_1400034a3:
  if (0 < iVar7) {
    iVar7 = iVar7 - ((int)_Dst - (int)pcVar1);
    *(int *)((longlong)param_2 + 0xc) = iVar7;
    if (0 < iVar7) {
      if ((uVar8 & 0x1c0) != 0) {
        *(int *)((longlong)param_2 + 0xc) = iVar7 + -1;
      }
      if ((iVar5 < 0) && ((uVar8 & 0x600) == 0x200)) {
        iVar5 = *(int *)((longlong)param_2 + 0xc);
        *(int *)((longlong)param_2 + 0xc) = iVar5 + -1;
        if (0 < iVar5) {
          *(undefined8 *)((longlong)auStack_70 + lVar4) = 0x140003698;
          memset(_Dst, 0x30, (longlong)iVar5);
          *(undefined4 *)((longlong)param_2 + 0xc) = 0xffffffff;
          _Dst = _Dst + iVar5;
        }
      } else if (((uVar8 & 0x400) == 0) &&
                 (iVar5 = *(int *)((longlong)param_2 + 0xc),
                  *(int *)((longlong)param_2 + 0xc) = iVar5 + -1, 0 < iVar5)) {
        do {
          *(undefined8 *)((longlong)auStack_70 + lVar4) = 0x1400036cd;
          FUN_140002a00(0x20, param_2);
          iVar5 = *(int *)((longlong)param_2 + 0xc);
          *(int *)((longlong)param_2 + 0xc) = iVar5 + -1;
        } while (0 < iVar5);
        uVar8 = *(uint *)(param_2 + 1);
      }
    }
  }
  if ((uVar8 & 0x80) == 0) {
    if ((uVar8 & 0x100) == 0) {
      if ((uVar8 & 0x40) != 0) {
        *_Dst = ' ';
        _Dst = _Dst + 1;
      }
    } else {
      *_Dst = '+';
      _Dst = _Dst + 1;
    }
  } else {
    *_Dst = '-';
    _Dst = _Dst + 1;
  }
  if (pcVar1 < _Dst) {
    do {
      _Dst = _Dst + -1;
      if (((uVar8 & 0x4000) == 0) &&
          (iVar5 = *(int *)((longlong)param_2 + 0x24),
           *(int *)(param_2 + 5) <= iVar5)) {
      LAB_14000350a:
        *(int *)((longlong)param_2 + 0x24) = iVar5 + 1;
      } else {
        cVar2 = *_Dst;
        pFVar3 = (FILE *)*param_2;
        if ((uVar8 & 0x2000) == 0) {
          *(char *)((longlong)&pFVar3->_ptr +
                    (longlong) * (int *)((longlong)param_2 + 0x24)) = cVar2;
          iVar5 = *(int *)((longlong)param_2 + 0x24);
          goto LAB_14000350a;
        }
        *(undefined8 *)((longlong)auStack_70 + lVar4) = 0x14000353f;
        fputc((int)cVar2, pFVar3);
        *(int *)((longlong)param_2 + 0x24) =
            *(int *)((longlong)param_2 + 0x24) + 1;
      }
      if (pcVar1 == _Dst)
        break;
      uVar8 = *(uint *)(param_2 + 1);
    } while (true);
  }
  iVar5 = *(int *)((longlong)param_2 + 0xc);
  while (true) {
    *(int *)((longlong)param_2 + 0xc) = iVar5 + -1;
    if (iVar5 < 1)
      break;
    if (((*(uint *)(param_2 + 1) & 0x4000) != 0) ||
        (iVar7 = *(int *)((longlong)param_2 + 0x24), iVar5 = iVar5 + -1,
         iVar7 < *(int *)(param_2 + 5))) {
      pFVar3 = (FILE *)*param_2;
      if ((*(uint *)(param_2 + 1) & 0x2000) == 0) {
        *(undefined1 *)((longlong)&pFVar3->_ptr +
                        (longlong) * (int *)((longlong)param_2 + 0x24)) = 0x20;
        iVar7 = *(int *)((longlong)param_2 + 0x24);
        iVar5 = *(int *)((longlong)param_2 + 0xc);
      } else {
        *(undefined8 *)((longlong)auStack_70 + lVar4) = 0x14000359a;
        fputc(0x20, pFVar3);
        iVar7 = *(int *)((longlong)param_2 + 0x24);
        iVar5 = *(int *)((longlong)param_2 + 0xc);
      }
    }
    *(int *)((longlong)param_2 + 0x24) = iVar7 + 1;
  }
  return;
}

void FUN_140003710(undefined8 *param_1)

{
  char cVar1;
  FILE *_File;
  int iVar2;
  ulonglong uVar3;
  longlong lVar4;
  lconv *plVar5;
  longlong lVar6;
  WCHAR WVar7;
  LPSTR pCVar8;
  LPSTR pCVar9;
  undefined8 auStack_60[5];
  CHAR aCStack_38[6];
  WCHAR local_32;
  byte local_30[8];

  if (*(int *)((longlong)param_1 + 0x14) == -3) {
    local_30[0] = 0;
    local_30[1] = 0;
    local_30[2] = 0;
    local_30[3] = 0;
    local_30[4] = 0;
    local_30[5] = 0;
    local_30[6] = 0;
    local_30[7] = 0;
    auStack_60[0] = 0x140003811;
    plVar5 = localeconv();
    auStack_60[0] = 0x140003826;
    lVar6 =
        FUN_140007c30(&local_32, (byte *)plVar5->decimal_point, 0x10, local_30);
    if ((int)lVar6 < 1) {
      local_32 = *(WCHAR *)(param_1 + 3);
    } else {
      *(WCHAR *)(param_1 + 3) = local_32;
    }
    *(int *)((longlong)param_1 + 0x14) = (int)lVar6;
    WVar7 = local_32;
  } else {
    WVar7 = *(WCHAR *)(param_1 + 3);
  }
  if (WVar7 == L'\0') {
    auStack_60[0] = 0x1400037ed;
    FUN_140002a00(0x2e, param_1);
    return;
  }
  auStack_60[0] = 0x14000374d;
  uVar3 = FUN_140002880();
  lVar6 = -uVar3;
  local_30[0] = 0;
  local_30[1] = 0;
  local_30[2] = 0;
  local_30[3] = 0;
  local_30[4] = 0;
  local_30[5] = 0;
  local_30[6] = 0;
  local_30[7] = 0;
  *(undefined8 *)((longlong)auStack_60 + lVar6) = 0x140003769;
  lVar4 = FUN_140007990(aCStack_38 + lVar6, WVar7);
  if ((int)lVar4 < 1) {
    *(undefined8 *)((longlong)auStack_60 + lVar6) = 0x14000384d;
    FUN_140002a00(0x2e, param_1);
  } else {
    pCVar8 = aCStack_38 + lVar6;
    do {
      while (true) {
        pCVar9 = pCVar8 + 1;
        if (((*(uint *)(param_1 + 1) & 0x4000) != 0) ||
            (iVar2 = *(int *)((longlong)param_1 + 0x24),
             iVar2 < *(int *)(param_1 + 5)))
          break;
      LAB_14000378a:
        *(int *)((longlong)param_1 + 0x24) = iVar2 + 1;
        pCVar8 = pCVar9;
        if (aCStack_38 + (ulonglong)((int)lVar4 - 1) + lVar6 + 1 == pCVar9) {
          return;
        }
      }
      cVar1 = *pCVar8;
      _File = (FILE *)*param_1;
      if ((*(uint *)(param_1 + 1) & 0x2000) == 0) {
        *(char *)((longlong)&_File->_ptr +
                  (longlong) * (int *)((longlong)param_1 + 0x24)) = cVar1;
        iVar2 = *(int *)((longlong)param_1 + 0x24);
        goto LAB_14000378a;
      }
      *(undefined8 *)((longlong)auStack_60 + lVar6) = 0x1400037bd;
      fputc((int)cVar1, _File);
      *(int *)((longlong)param_1 + 0x24) =
          *(int *)((longlong)param_1 + 0x24) + 1;
      pCVar8 = pCVar9;
    } while (aCStack_38 + (ulonglong)((int)lVar4 - 1) + lVar6 + 1 != pCVar9);
  }
  return;
}

void FUN_140003860(int param_1, char *param_2, int param_3, undefined8 *param_4)

{
  char cVar1;
  int iVar2;
  int iVar3;
  uint uVar4;

  iVar2 = *(int *)((longlong)param_4 + 0xc);
  if (param_3 < 1) {
    if (iVar2 < 1) {
      if ((iVar2 != 0) || (-1 < *(int *)(param_4 + 2)))
        goto LAB_1400039e7;
      iVar2 = -*(int *)(param_4 + 2);
      *(int *)((longlong)param_4 + 0xc) = iVar2;
      if ((*(byte *)((longlong)param_4 + 9) & 8) != 0)
        goto LAB_1400038a1;
    LAB_1400038bc:
      if (param_1 == 0) {
        uVar4 = *(uint *)(param_4 + 1);
        if ((uVar4 & 0x1c0) != 0) {
          *(int *)((longlong)param_4 + 0xc) = iVar2 + -1;
          if ((iVar2 + -1 != 0) && ((uVar4 & 0x600) == 0))
            goto LAB_140003ac3;
          goto LAB_14000390e;
        }
        if ((uVar4 & 0x600) == 0) {
          iVar2 = iVar2 + -1;
          goto LAB_140003ac6;
        }
        goto LAB_140003930;
      }
      *(int *)((longlong)param_4 + 0xc) = iVar2 + -1;
      if ((iVar2 + -1 != 0) && ((*(uint *)(param_4 + 1) & 0x600) == 0)) {
      LAB_140003ac3:
        iVar2 = iVar2 + -2;
      LAB_140003ac6:
        *(int *)((longlong)param_4 + 0xc) = iVar2;
        do {
          FUN_140002a00(0x20, param_4);
          iVar2 = *(int *)((longlong)param_4 + 0xc);
          *(int *)((longlong)param_4 + 0xc) = iVar2 + -1;
        } while (0 < iVar2);
        goto LAB_140003903;
      }
    } else {
      iVar3 = *(int *)(param_4 + 2);
      iVar2 = iVar2 + -1;
      if (iVar3 < iVar2)
        goto LAB_140003894;
    LAB_1400039e7:
      *(undefined4 *)((longlong)param_4 + 0xc) = 0xffffffff;
      if (param_1 == 0)
        goto LAB_14000390b;
    }
  LAB_140003a00:
    FUN_140002a00(0x2d, param_4);
  } else {
    if (iVar2 < param_3) {
      *(undefined4 *)((longlong)param_4 + 0xc) = 0xffffffff;
      if (((*(byte *)((longlong)param_4 + 9) & 0x10) != 0) &&
          (*(short *)(param_4 + 4) != 0)) {
        iVar2 = -1;
      LAB_140003b41:
        iVar3 = ((param_3 + 2U) / 3 - 1) - iVar2;
        if ((param_3 + 2U) / 3 != 1) {
          do {
            if (iVar2 < 1)
              goto LAB_140003903;
            iVar2 = iVar2 + -1;
            *(int *)((longlong)param_4 + 0xc) = iVar2;
          } while (iVar3 + iVar2 != 0);
        }
        goto LAB_1400038b8;
      }
    } else {
      iVar3 = *(int *)(param_4 + 2);
      iVar2 = iVar2 - param_3;
      if (iVar3 < iVar2) {
      LAB_140003894:
        iVar2 = iVar2 - iVar3;
        *(int *)((longlong)param_4 + 0xc) = iVar2;
        if ((iVar3 < 1) && ((*(uint *)(param_4 + 1) & 0x800) == 0)) {
          if ((param_3 < 1) || ((*(uint *)(param_4 + 1) & 0x1000) == 0))
            goto LAB_1400038bc;
        } else {
        LAB_1400038a1:
          iVar2 = iVar2 + -1;
          *(int *)((longlong)param_4 + 0xc) = iVar2;
          if ((param_3 < 1) || ((*(byte *)((longlong)param_4 + 9) & 0x10) == 0))
            goto LAB_1400038b8;
        }
      LAB_140003bb7:
        if (*(short *)(param_4 + 4) != 0)
          goto LAB_140003b41;
      } else {
        *(undefined4 *)((longlong)param_4 + 0xc) = 0xffffffff;
        iVar2 = -1;
        if ((*(byte *)((longlong)param_4 + 9) & 0x10) != 0)
          goto LAB_140003bb7;
      }
    LAB_1400038b8:
      if (0 < iVar2)
        goto LAB_1400038bc;
    }
  LAB_140003903:
    if (param_1 != 0)
      goto LAB_140003a00;
  LAB_14000390b:
    uVar4 = *(uint *)(param_4 + 1);
  LAB_14000390e:
    if ((uVar4 & 0x100) == 0) {
      if ((uVar4 & 0x40) != 0) {
        FUN_140002a00(0x20, param_4);
      }
    } else {
      FUN_140002a00(0x2b, param_4);
    }
  }
LAB_140003930:
  if ((0 < *(int *)((longlong)param_4 + 0xc)) &&
      ((*(uint *)(param_4 + 1) & 0x600) == 0x200)) {
    *(int *)((longlong)param_4 + 0xc) = *(int *)((longlong)param_4 + 0xc) + -1;
    do {
      FUN_140002a00(0x30, param_4);
      iVar2 = *(int *)((longlong)param_4 + 0xc);
      *(int *)((longlong)param_4 + 0xc) = iVar2 + -1;
    } while (0 < iVar2);
  }
  if (param_3 < 1) {
    FUN_140002a00(0x30, param_4);
    iVar2 = *(int *)(param_4 + 2);
    if ((0 < iVar2) || ((*(byte *)((longlong)param_4 + 9) & 8) != 0))
      goto LAB_140003a78;
    if (param_3 == 0)
      goto LAB_1400039b9;
  } else {
    while (true) {
      cVar1 = *param_2;
      iVar2 = 0x30;
      if (cVar1 != '\0') {
        param_2 = param_2 + 1;
        iVar2 = (int)cVar1;
      }
      FUN_140002a00(iVar2, param_4);
      param_3 = param_3 + -1;
      if (param_3 == 0)
        break;
      if ((((*(byte *)((longlong)param_4 + 9) & 0x10) != 0) &&
           (*(short *)(param_4 + 4) != 0)) &&
          ((uint)(param_3 * -0x55555555) < 0x55555556)) {
        FUN_140002a60((longlong)(param_4 + 4), 1, param_4);
      }
    }
    iVar2 = *(int *)(param_4 + 2);
    if (0 < iVar2) {
      FUN_140003710(param_4);
      goto LAB_140003a43;
    }
    param_3 = 0;
    if ((*(byte *)((longlong)param_4 + 9) & 8) == 0) {
    LAB_1400039b9:
      *(int *)(param_4 + 2) = iVar2 + -1;
      return;
    }
  LAB_140003a78:
    FUN_140003710(param_4);
    if (param_3 == 0)
      goto LAB_140003a43;
    iVar2 = *(int *)(param_4 + 2);
  }
  *(int *)(param_4 + 2) = iVar2 + param_3;
  do {
    FUN_140002a00(0x30, param_4);
    param_3 = param_3 + 1;
  } while (param_3 != 0);
LAB_140003a43:
  while (iVar2 = *(int *)(param_4 + 2), *(int *)(param_4 + 2) = iVar2 + -1,
         0 < iVar2) {
    cVar1 = *param_2;
    iVar2 = 0x30;
    if (cVar1 != '\0') {
      param_2 = param_2 + 1;
      iVar2 = (int)cVar1;
    }
    FUN_140002a00(iVar2, param_4);
  }
  return;
}

void FUN_140003c40(int param_1, char *param_2, int param_3, undefined8 *param_4)

{
  uint uVar1;
  ulonglong uVar2;
  int iVar3;
  int iVar4;

  iVar4 = 1;
  iVar3 = param_3 + -1;
  uVar2 = (ulonglong)iVar3;
  while (iVar3 = iVar3 / 10, iVar3 != 0) {
    iVar4 = iVar4 + 1;
  }
  iVar3 = *(int *)((longlong)param_4 + 0x2c);
  if (iVar3 == -1) {
    *(undefined4 *)((longlong)param_4 + 0x2c) = 2;
    iVar3 = 2;
  }
  if (iVar3 <= iVar4) {
    iVar3 = iVar4;
  }
  iVar4 = *(int *)((longlong)param_4 + 0xc) - (iVar3 + 2);
  if (*(int *)((longlong)param_4 + 0xc) <= iVar3 + 2) {
    iVar4 = -1;
  }
  *(int *)((longlong)param_4 + 0xc) = iVar4;
  FUN_140003860(param_1, param_2, 1, param_4);
  uVar1 = *(uint *)(param_4 + 1);
  *(undefined4 *)(param_4 + 2) = *(undefined4 *)((longlong)param_4 + 0x2c);
  *(uint *)(param_4 + 1) = uVar1 | 0x1c0;
  FUN_140002a00(uVar1 & 0x20 | 0x45, param_4);
  *(int *)((longlong)param_4 + 0xc) =
      *(int *)((longlong)param_4 + 0xc) + iVar3 + 1;
  FUN_140003360(uVar2, param_4);
  return;
}

void FUN_140003d10(undefined1 (*param_1)[10], undefined8 *param_2)

{
  char *pcVar1;
  uint uVar2;
  undefined1 local_38[2][10];
  uint local_20;
  uint local_1c[3];

  local_38[0] = *param_1;
  if (*(int *)(param_2 + 2) < 0) {
    *(undefined4 *)(param_2 + 2) = 6;
    uVar2 = 7;
  } else {
    uVar2 = *(int *)(param_2 + 2) + 1;
  }
  pcVar1 = (char *)FUN_140002910(2, (ulonglong *)local_38, uVar2, local_1c,
                                 &local_20);
  if (local_1c[0] != 0xffff8000) {
    FUN_140003c40(local_20, pcVar1, local_1c[0], param_2);
    FUN_140005060((longlong)pcVar1);
    return;
  }
  FUN_140002d90(local_20, (longlong)pcVar1, param_2);
  FUN_140005060((longlong)pcVar1);
  return;
}

void FUN_140003db0(undefined1 (*param_1)[10], undefined8 *param_2)

{
  int iVar1;
  char *pcVar2;
  int iVar3;
  uint uVar4;
  undefined1 local_38[2][10];
  uint local_20;
  uint local_1c[3];

  uVar4 = *(uint *)(param_2 + 2);
  local_38[0] = *param_1;
  if ((int)uVar4 < 0) {
    *(undefined4 *)(param_2 + 2) = 6;
    uVar4 = 6;
  }
  pcVar2 = (char *)FUN_140002910(3, (ulonglong *)local_38, uVar4, local_1c,
                                 &local_20);
  if (local_1c[0] == 0xffff8000) {
    FUN_140002d90(local_20, (longlong)pcVar2, param_2);
  } else {
    FUN_140003860(local_20, pcVar2, local_1c[0], param_2);
    iVar1 = *(int *)((longlong)param_2 + 0xc);
    while (true) {
      *(int *)((longlong)param_2 + 0xc) = iVar1 + -1;
      if (iVar1 < 1)
        break;
      if (((*(uint *)(param_2 + 1) & 0x4000) != 0) ||
          (iVar3 = *(int *)((longlong)param_2 + 0x24), iVar1 = iVar1 + -1,
           iVar3 < *(int *)(param_2 + 5))) {
        if ((*(uint *)(param_2 + 1) & 0x2000) == 0) {
          *(undefined1 *)((longlong) &
                          ((FILE *)*param_2)->_ptr +
                              (longlong) * (int *)((longlong)param_2 + 0x24)) =
              0x20;
          iVar3 = *(int *)((longlong)param_2 + 0x24);
          iVar1 = *(int *)((longlong)param_2 + 0xc);
        } else {
          fputc(0x20, (FILE *)*param_2);
          iVar3 = *(int *)((longlong)param_2 + 0x24);
          iVar1 = *(int *)((longlong)param_2 + 0xc);
        }
      }
      *(int *)((longlong)param_2 + 0x24) = iVar3 + 1;
    }
  }
  FUN_140005060((longlong)pcVar2);
  return;
}

void FUN_140003e90(undefined1 (*param_1)[10], undefined8 *param_2)

{
  int iVar1;
  char *_Str;
  size_t sVar2;
  uint uVar3;
  undefined1 local_38[2][10];
  uint local_20;
  uint local_1c;

  uVar3 = *(uint *)(param_2 + 2);
  local_38[0] = *param_1;
  if ((int)uVar3 < 0) {
    *(undefined4 *)(param_2 + 2) = 6;
    uVar3 = 6;
  } else if (uVar3 == 0) {
    *(undefined4 *)(param_2 + 2) = 1;
    uVar3 = 1;
  }
  _Str = (char *)FUN_140002910(2, (ulonglong *)local_38, uVar3, &local_1c,
                               &local_20);
  if (local_1c != 0xffff8000) {
    if ((-4 < (int)local_1c) && ((int)local_1c <= *(int *)(param_2 + 2))) {
      if ((*(uint *)(param_2 + 1) & 0x800) == 0) {
        sVar2 = strlen(_Str);
        iVar1 = (int)sVar2 - local_1c;
        *(int *)(param_2 + 2) = iVar1;
        if ((iVar1 < 0) && (0 < *(int *)((longlong)param_2 + 0xc))) {
          *(int *)((longlong)param_2 + 0xc) =
              iVar1 + *(int *)((longlong)param_2 + 0xc);
        }
      } else {
        *(uint *)(param_2 + 2) = *(int *)(param_2 + 2) - local_1c;
      }
      FUN_140003860(local_20, _Str, local_1c, param_2);
      while (iVar1 = *(int *)((longlong)param_2 + 0xc),
             *(int *)((longlong)param_2 + 0xc) = iVar1 + -1, 0 < iVar1) {
        FUN_140002a00(0x20, param_2);
      }
      FUN_140005060((longlong)_Str);
      return;
    }
    if ((*(uint *)(param_2 + 1) & 0x800) == 0) {
      sVar2 = strlen(_Str);
      iVar1 = (int)sVar2;
    } else {
      iVar1 = *(int *)(param_2 + 2);
    }
    *(int *)(param_2 + 2) = iVar1 + -1;
    FUN_140003c40(local_20, _Str, local_1c, param_2);
    FUN_140005060((longlong)_Str);
    return;
  }
  FUN_140002d90(local_20, (longlong)_Str, param_2);
  FUN_140005060((longlong)_Str);
  return;
}

void FUN_140004010(ulonglong param_1, short param_2, undefined8 *param_3)

{
  char cVar1;
  byte bVar2;
  uint uVar3;
  ulonglong uVar4;
  uint uVar5;
  int iVar6;
  int iVar7;
  ulonglong uVar8;
  byte *pbVar9;
  short sVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  short local_5a;
  byte local_58;
  byte local_57[39];

  uVar5 = *(uint *)(param_3 + 2);
  cVar1 = (char)uVar5;
  if ((param_2 == 0) && (param_1 == 0)) {
    if (uVar5 < 0xf) {
      uVar8 = 0;
      sVar10 = 0;
      uVar4 = 4L << (('\x0e' - cVar1) * '\x04' & 0x3fU);
    LAB_140004142:
      param_1 = uVar4 * 2 >> (('\x0f' - cVar1) * '\x04' & 0x3fU);
      if ((param_1 == 0) && (uVar5 == 0))
        goto LAB_140004160;
    LAB_140004114:
      iVar6 = uVar5 + 1;
    } else {
      if ((int)uVar5 < 1) {
        uVar5 = *(uint *)(param_3 + 1);
        uVar8 = 0;
        sVar10 = 0;
        goto LAB_140004168;
      }
      uVar8 = 0;
      sVar10 = 0;
      param_1 = 0;
      iVar6 = 0x10;
    }
  LAB_140004054:
    uVar5 = *(uint *)(param_3 + 1);
    pbVar9 = &local_58;
    do {
      uVar3 = (uint)param_1 & 0xf;
      cVar1 = (char)uVar3;
      if (iVar6 == 1) {
        if (((&local_58 < pbVar9) || ((uVar5 & 0x800) != 0)) ||
            (0 < *(int *)(param_3 + 2))) {
          *pbVar9 = 0x2e;
          pbVar9 = pbVar9 + 1;
          goto LAB_1400040c2;
        }
        if ((param_1 & 0xf) == 0) {
          if (*(int *)(param_3 + 2) == 0) {
            *pbVar9 = 0x30;
            pbVar9 = pbVar9 + 1;
          }
          break;
        }
      LAB_1400040c6:
        if (uVar3 < 10) {
        LAB_140004088:
          bVar2 = cVar1 + 0x30;
        } else {
          bVar2 = cVar1 + 0x37U | (byte)uVar5 & 0x20;
        }
        *pbVar9 = bVar2;
        pbVar9 = pbVar9 + 1;
      } else {
        if (0 < *(int *)(param_3 + 2)) {
          *(int *)(param_3 + 2) = *(int *)(param_3 + 2) + -1;
        }
      LAB_1400040c2:
        if ((param_1 & 0xf) != 0)
          goto LAB_1400040c6;
        if ((&local_58 < pbVar9) || (-1 < *(int *)(param_3 + 2)))
          goto LAB_140004088;
      }
      param_1 = param_1 >> 4;
      iVar6 = iVar6 + -1;
    } while (iVar6 != 0);
    if (pbVar9 == &local_58) {
      if (*(int *)(param_3 + 2) < 1)
        goto LAB_140004168;
      goto LAB_140004170;
    }
    iVar6 = *(int *)((longlong)param_3 + 0xc);
  } else {
    sVar10 = param_2 + -3;
    if (uVar5 < 0xf) {
      uVar4 = (4L << (('\x0e' - cVar1) * '\x04' & 0x3fU)) + (param_1 >> 1);
      if (-1 < (longlong)uVar4) {
        uVar8 = (ulonglong)sVar10;
        goto LAB_140004142;
      }
      sVar10 = param_2 + 1;
      uVar8 = (ulonglong)sVar10;
      param_1 = (uVar4 >> 3) >> (('\x0f' - cVar1) * '\x04' & 0x3fU);
      goto LAB_140004114;
    }
    uVar8 = (ulonglong)sVar10;
    iVar6 = 0x10;
    if ((param_1 != 0) || (0 < (int)uVar5))
      goto LAB_140004054;
  LAB_140004160:
    uVar5 = *(uint *)(param_3 + 1);
  LAB_140004168:
    pbVar9 = &local_58;
    if ((uVar5 & 0x800) != 0) {
    LAB_140004170:
      local_58 = 0x2e;
      pbVar9 = local_57;
    }
    iVar6 = *(int *)((longlong)param_3 + 0xc);
    *pbVar9 = 0x30;
    pbVar9 = pbVar9 + 1;
  }
  iVar13 = 2;
  if (0 < iVar6) {
    iVar13 = 2;
    iVar7 = (int)pbVar9 - (int)&local_58;
    if (0 < *(int *)(param_3 + 2)) {
      iVar7 = *(int *)(param_3 + 2) + iVar7;
    }
    iVar11 = (iVar7 + 6) - (uint)((uVar5 & 0x1c0) == 0);
    iVar7 = (int)sVar10 / 10 - ((int)sVar10 >> 0x1f);
    iVar12 = iVar11;
    if (iVar7 != 0) {
      do {
        iVar12 = iVar12 + 1;
        iVar7 = iVar7 / 10;
      } while (iVar7 != 0);
      iVar13 = (int)(short)(((short)iVar12 - (short)iVar11) + 2);
    }
    if (iVar12 < iVar6) {
      iVar6 = iVar6 - iVar12;
      if ((uVar5 & 0x600) == 0) {
        *(int *)((longlong)param_3 + 0xc) = iVar6 + -1;
        do {
          FUN_140002a00(0x20, param_3);
          iVar6 = *(int *)((longlong)param_3 + 0xc);
          *(int *)((longlong)param_3 + 0xc) = iVar6 + -1;
        } while (0 < iVar6);
        uVar5 = *(uint *)(param_3 + 1);
        goto joined_r0x000140004197;
      }
    } else {
      iVar6 = -1;
    }
    *(int *)((longlong)param_3 + 0xc) = iVar6;
  }
joined_r0x000140004197:
  if ((uVar5 & 0x80) == 0) {
    if ((uVar5 & 0x100) == 0) {
      if ((uVar5 & 0x40) != 0) {
        FUN_140002a00(0x20, param_3);
      }
    } else {
      FUN_140002a00(0x2b, param_3);
    }
  } else {
    FUN_140002a00(0x2d, param_3);
  }
  FUN_140002a00(0x30, param_3);
  FUN_140002a00(*(uint *)(param_3 + 1) & 0x20 | 0x58, param_3);
  if ((0 < *(int *)((longlong)param_3 + 0xc)) &&
      ((*(byte *)((longlong)param_3 + 9) & 2) != 0)) {
    *(int *)((longlong)param_3 + 0xc) = *(int *)((longlong)param_3 + 0xc) + -1;
    do {
      FUN_140002a00(0x30, param_3);
      iVar6 = *(int *)((longlong)param_3 + 0xc);
      *(int *)((longlong)param_3 + 0xc) = iVar6 + -1;
    } while (0 < iVar6);
  }
  if (&local_58 < pbVar9) {
    do {
      iVar6 = (int)(char)pbVar9[-1];
      pbVar9 = pbVar9 + -1;
      if (iVar6 == 0x2e) {
        FUN_140003710(param_3);
      } else if (iVar6 == 0x2c) {
        local_5a = *(short *)(param_3 + 4);
        if (local_5a != 0) {
          FUN_140002a60((longlong)&local_5a, 1, param_3);
        }
      } else {
        FUN_140002a00(iVar6, param_3);
      }
    } while (pbVar9 != &local_58);
  }
  while (iVar6 = *(int *)(param_3 + 2), *(int *)(param_3 + 2) = iVar6 + -1,
         0 < iVar6) {
    FUN_140002a00(0x30, param_3);
  }
  FUN_140002a00(*(uint *)(param_3 + 1) & 0x20 | 0x50, param_3);
  *(int *)((longlong)param_3 + 0xc) =
      *(int *)((longlong)param_3 + 0xc) + iVar13;
  *(uint *)(param_3 + 1) = *(uint *)(param_3 + 1) | 0x1c0;
  FUN_140003360(uVar8, param_3);
  return;
}

uint FUN_1400044d0(uint param_1, FILE *param_2, int param_3, char *param_4,
                   ulonglong *param_5)

{
  int iVar1;
  uint uVar2;
  byte bVar3;
  uint uVar4;
  int extraout_EAX;
  int *piVar5;
  char *pcVar6;
  lconv *plVar7;
  longlong lVar8;
  size_t sVar9;
  uint uVar10;
  int iVar11;
  ulonglong *puVar12;
  ulonglong uVar13;
  undefined1(*pauVar14)[10];
  ushort uVar15;
  byte *pbVar16;
  byte *pbVar17;
  wchar_t *_Str;
  byte *pbVar18;
  uint uVar19;
  int iVar20;
  uint *puVar21;
  float10 fVar22;
  ulonglong local_c8;
  ushort uStack_c0;
  undefined1 local_a8[3][10];
  WCHAR local_8a;
  ulonglong local_88[2];
  FILE *local_78;
  uint local_70;
  uint local_6c;
  uint auStack_68[2];
  undefined2 local_60;
  int local_5c;
  WCHAR local_58;
  uint local_54;
  int local_50;
  undefined4 local_4c;

  piVar5 = _errno();
  uVar10 = (uint)*param_4;
  uVar19 = param_1 & 0x6000;
  iVar1 = *piVar5;
  local_50 = param_3;
  pbVar16 = (byte *)(param_4 + 1);
  auStack_68[0] = 0xffffffff;
  auStack_68[1] = 0xfffffffd;
  local_60 = 0;
  local_6c = 0xffffffff;
  local_5c = 0;
  local_58 = L'\0';
  local_54 = 0;
  local_4c = 0xffffffff;
  if (*param_4 == '\0') {
    return uVar10;
  }
  uVar4 = uVar10;
  local_78 = param_2;
  local_70 = uVar19;
LAB_1400045ce:
  uVar2 = local_54;
  if (uVar10 == 0x25) {
    bVar3 = *pbVar16;
    local_6c = 0xffffffff;
    auStack_68[0] = 0xffffffff;
    if (bVar3 == 0) {
      return local_54;
    }
    iVar20 = 0;
    uVar10 = 0;
    pbVar17 = pbVar16;
    puVar21 = &local_6c;
    local_70 = uVar19;
    do {
      pbVar18 = pbVar17 + 1;
      iVar11 = (int)(char)bVar3;
      puVar12 = param_5;
      switch (bVar3) {
      case 0x20:
        if (uVar10 != 0)
          goto LAB_140004670;
        bVar3 = pbVar17[1];
        local_70 = local_70 | 0x40;
        break;
      default:
        if ((9 < (byte)(bVar3 - 0x30)) || (3 < uVar10)) {
        LAB_140004847:
          FUN_140002a00(0x25, &local_78);
          pbVar18 = pbVar16;
          goto LAB_1400045bc;
        }
        if (uVar10 == 0) {
          uVar10 = 1;
        } else {
        LAB_140004d8f:
          if (uVar10 == 2) {
            uVar10 = 3;
          }
        }
        if (puVar21 != (uint *)0x0) {
          if ((int)*puVar21 < 0) {
            bVar3 = pbVar17[1];
            *puVar21 = iVar11 - 0x30;
            break;
          }
          *puVar21 = iVar11 + -0x30 + *puVar21 * 10;
        }
      LAB_140004670:
        bVar3 = pbVar17[1];
        break;
      case 0x23:
        if (uVar10 != 0)
          goto LAB_140004670;
        bVar3 = pbVar17[1];
        local_70 = local_70 | 0x800;
        break;
      case 0x25:
        goto switchD_140004610_caseD_25;
      case 0x27:
        if (uVar10 != 0)
          goto LAB_140004670;
        local_70 = local_70 | 0x1000;
        local_88[0] = local_88[0] & 0xffffffff00000000;
        plVar7 = localeconv();
        lVar8 = FUN_140007c30(&local_8a, (byte *)plVar7->thousands_sep, 0x10,
                              (byte *)local_88);
        if (0 < (int)lVar8) {
          local_58 = local_8a;
        }
        local_5c = (int)lVar8;
        bVar3 = pbVar17[1];
        break;
      case 0x2a:
        if (puVar21 == (uint *)0x0) {
        LAB_140004a49:
          bVar3 = pbVar17[1];
          uVar10 = 4;
        } else if ((uVar10 & 0xfffffffd) == 0) {
          uVar13 = *param_5;
          param_5 = param_5 + 1;
          *puVar21 = (uint)uVar13;
          if ((int)(uint)uVar13 < 0) {
            if (uVar10 != 0) {
              bVar3 = pbVar17[1];
              puVar21 = (uint *)0x0;
              auStack_68[0] = 0xffffffff;
              uVar10 = 2;
              break;
            }
            local_70 = local_70 | 0x400;
            local_6c = -local_6c;
          }
          bVar3 = pbVar17[1];
          puVar21 = (uint *)0x0;
        } else {
          bVar3 = pbVar17[1];
          puVar21 = (uint *)0x0;
          uVar10 = 4;
        }
        break;
      case 0x2b:
        if (uVar10 != 0)
          goto LAB_140004670;
        bVar3 = pbVar17[1];
        local_70 = local_70 | 0x100;
        break;
      case 0x2d:
        if (uVar10 != 0)
          goto LAB_140004670;
        bVar3 = pbVar17[1];
        local_70 = local_70 | 0x400;
        break;
      case 0x2e:
        if (1 < uVar10)
          goto LAB_140004a49;
        bVar3 = pbVar17[1];
        uVar10 = 2;
        auStack_68[0] = 0;
        puVar21 = auStack_68;
        break;
      case 0x30:
        if (uVar10 != 0) {
          if (uVar10 < 4) {
            iVar11 = 0x30;
            goto LAB_140004d8f;
          }
          goto LAB_140004847;
        }
        bVar3 = pbVar17[1];
        local_70 = local_70 | 0x200;
        break;
      case 0x41:
        puVar12 = (ulonglong *)*param_5;
        if ((local_70 & 4) != 0)
          goto LAB_14000488e;
      LAB_140004a88:
        uVar10 = (uint)puVar12;
        uVar4 = (uint)((ulonglong)puVar12 >> 0x20);
        if (-1 < (int)(0x7ff00000 -
                       ((-uVar10 | uVar10) >> 0x1f | uVar4 & 0x7fffffff))) {
          fVar22 = (float10)(double)puVar12;
          local_c8 = SUB108(fVar22, 0);
          uStack_c0 = (ushort)((unkuint10)fVar22 >> 0x40);
          if ((short)uStack_c0 < 0) {
            local_70 = local_70 | 0x80;
          }
          if (((uVar4 & 0x7ff00000) == 0x7ff00000 &&
               (((ulonglong)puVar12 & 0xfffff00000000) == 0 && uVar10 == 0)) &&
              ((((ulonglong)puVar12 & 0xfffff00000000) != 0 || uVar10 != 0) ||
               ((ulonglong)puVar12 & 0x7ff0000000000000) != 0)) {
            FUN_140002d90(uStack_c0 & 0x8000, 0x14000af8a, &local_78);
            goto LAB_1400049a0;
          }
          uStack_c0 = uStack_c0 & 0x7fff;
          if (((unkuint10)fVar22 & 0x7fff) == 0) {
          LAB_140004e1f:
            if (local_c8 != 0) {
              uStack_c0 = 0xfc05;
            }
          } else {
            if (uStack_c0 < 0x3c01) {
              local_c8 = local_c8 >> ((byte)(0x3c01 - uStack_c0) & 0x3f);
              uStack_c0 = uStack_c0 + (0x3c01 - uStack_c0);
            } else if (((unkuint10)fVar22 & 0x7fff) == 0)
              goto LAB_140004e1f;
            uStack_c0 = uStack_c0 + 0xc004;
          }
          local_c8 = local_c8 >> 3;
          goto LAB_140004d27;
        }
      LAB_140004da1:
        FUN_140002d90(0, 0x14000af86, &local_78);
        goto LAB_1400049a0;
      case 0x43:
        goto LAB_140004b2f;
      case 0x45:
        pauVar14 = (undefined1(*)[10]) * param_5;
        if ((local_70 & 4) != 0)
          goto LAB_1400049f1;
      LAB_140004b67:
        local_a8[0] = (undefined1[10])(float10)(double)pauVar14;
        FUN_140003d10(local_a8, &local_78);
        goto LAB_1400049a0;
      case 0x46:
        pauVar14 = (undefined1(*)[10]) * param_5;
        if ((local_70 & 4) != 0)
          goto LAB_1400049c3;
      LAB_140004b98:
        local_a8[0] = (undefined1[10])(float10)(double)pauVar14;
        FUN_140003db0(local_a8, &local_78);
        goto LAB_1400049a0;
      case 0x47:
        pauVar14 = (undefined1(*)[10]) * param_5;
        if ((local_70 & 4) != 0)
          goto LAB_14000498b;
      LAB_140004bc9:
        local_a8[0] = (undefined1[10])(float10)(double)pauVar14;
        FUN_140003e90(local_a8, &local_78);
        goto LAB_1400049a0;
      case 0x49:
        bVar3 = pbVar17[1];
        if (bVar3 == 0x36) {
          if (pbVar17[2] != 0x34)
            goto LAB_140004847;
          bVar3 = pbVar17[3];
          iVar20 = 3;
          pbVar18 = pbVar17 + 3;
          uVar10 = 4;
        } else if (bVar3 == 0x33) {
          if (pbVar17[2] != 0x32)
            goto LAB_140004847;
          bVar3 = pbVar17[3];
          iVar20 = 2;
          pbVar18 = pbVar17 + 3;
          uVar10 = 4;
        } else {
          iVar20 = 3;
          uVar10 = 4;
        }
        break;
      case 0x4c:
        bVar3 = pbVar17[1];
        local_70 = local_70 | 4;
        uVar10 = 4;
        break;
      case 0x53:
        goto LAB_140004d3a;
      case 0x58:
      case 0x6f:
      case 0x75:
      case 0x78:
        local_70 = local_70 & 0xfffffeff;
        if (iVar20 == 3) {
          local_88[0] = *param_5;
        } else if (iVar20 == 2) {
          local_88[0] = (ulonglong)(uint)*param_5;
        } else {
          uVar10 = (uint)*param_5;
          if (iVar20 == 1) {
            local_88[0] = (ulonglong)(uVar10 & 0xffff);
          } else {
            local_88[0] = (ulonglong)(uVar10 & 0xff);
            if (iVar20 != 5) {
              local_88[0] = (ulonglong)uVar10;
            }
          }
        }
        if (iVar11 == 0x75) {
          FUN_140003360(local_88[0], &local_78);
        } else {
          FUN_140002e30(iVar11, local_88[0], &local_78);
        }
        goto LAB_1400049a0;
      case 0x61:
        puVar12 = (ulonglong *)*param_5;
        uVar4 = local_70 | 0x20;
        uVar10 = local_70 & 4;
        local_70 = uVar4;
        if (uVar10 == 0)
          goto LAB_140004a88;
      LAB_14000488e:
        local_c8 = *puVar12;
        uVar15 = (ushort)(uint)puVar12[1];
        uVar10 = (uint)(local_c8 >> 0x20) & 0x7fffffff | (uint)local_c8;
        if (0xfffe - ((-uVar10 | uVar10) >> 0x1f |
                      (short)uVar15 * 2 & 0xffffU) >>
                0x10 !=
            0)
          goto LAB_140004da1;
        if ((short)uVar15 < 0) {
          local_70 = local_70 | 0x80;
        }
        uStack_c0 = uVar15 & 0x7fff;
        if (((uint)puVar12[1] & 0x7fff) == 0) {
          if (local_c8 != 0) {
            uStack_c0 = 0xc002;
          }
        } else {
          if ((uStack_c0 == 0x7fff) && (uVar10 == 0)) {
            FUN_140002d90((int)(short)uVar15 & 0x8000, 0x14000af8a, &local_78);
            goto LAB_1400049a0;
          }
          uStack_c0 = uStack_c0 + 0xc001;
        }
      LAB_140004d27:
        FUN_140004010(local_c8, uStack_c0, &local_78);
        goto LAB_1400049a0;
      case 99:
        auStack_68[0] = 0xffffffff;
        if (iVar20 - 2U < 2) {
        LAB_140004b2f:
          auStack_68[0] = 0xffffffff;
          local_88[0] = CONCAT62(local_88[0]._2_6_, (short)(uint)*param_5);
          FUN_140002a60((longlong)local_88, 1, &local_78);
          puVar12 = param_5 + 1;
        } else {
          local_88[0] = CONCAT71(local_88[0]._1_7_, (char)(uint)*param_5);
          FUN_140002bf0((char *)local_88, 1, &local_78);
          puVar12 = param_5 + 1;
        }
        goto LAB_1400045bc;
      case 100:
      case 0x69:
        local_70 = local_70 | 0x80;
        if (iVar20 == 3) {
          uVar13 = *param_5;
        } else {
          uVar10 = (uint)*param_5;
          uVar13 = (longlong)(int)uVar10;
          if (iVar20 != 2) {
            if (iVar20 == 1) {
              uVar13 = (ulonglong)(short)uVar10;
            } else if (iVar20 == 5) {
              uVar13 = (longlong)(char)uVar10;
            }
          }
        }
        FUN_140003360(uVar13, &local_78);
        puVar12 = param_5 + 1;
        goto LAB_1400045bc;
      case 0x65:
        pauVar14 = (undefined1(*)[10]) * param_5;
        uVar4 = local_70 | 0x20;
        uVar10 = local_70 & 4;
        local_70 = uVar4;
        if (uVar10 == 0)
          goto LAB_140004b67;
      LAB_1400049f1:
        local_a8[0] = *pauVar14;
        FUN_140003d10(local_a8, &local_78);
        goto LAB_1400049a0;
      case 0x66:
        pauVar14 = (undefined1(*)[10]) * param_5;
        uVar4 = local_70 | 0x20;
        uVar10 = local_70 & 4;
        local_70 = uVar4;
        if (uVar10 == 0)
          goto LAB_140004b98;
      LAB_1400049c3:
        local_a8[0] = *pauVar14;
        FUN_140003db0(local_a8, &local_78);
        goto LAB_1400049a0;
      case 0x67:
        pauVar14 = (undefined1(*)[10]) * param_5;
        uVar4 = local_70 | 0x20;
        uVar10 = local_70 & 4;
        local_70 = uVar4;
        if (uVar10 == 0)
          goto LAB_140004bc9;
      LAB_14000498b:
        local_a8[0] = *pauVar14;
        FUN_140003e90(local_a8, &local_78);
        goto LAB_1400049a0;
      case 0x68:
        bVar3 = pbVar17[1];
        if (bVar3 == 0x68) {
          bVar3 = pbVar17[2];
          iVar20 = 5;
          pbVar18 = pbVar17 + 2;
          uVar10 = 4;
        } else {
          iVar20 = 1;
          uVar10 = 4;
        }
        break;
      case 0x6a:
      case 0x74:
      case 0x7a:
        bVar3 = pbVar17[1];
        iVar20 = 3;
        uVar10 = 4;
        break;
      case 0x6c:
        bVar3 = pbVar17[1];
        if (bVar3 == 0x6c) {
          bVar3 = pbVar17[2];
          iVar20 = 3;
          pbVar18 = pbVar17 + 2;
          uVar10 = 4;
        } else {
          iVar20 = 2;
          uVar10 = 4;
        }
        break;
      case 0x6d:
        pcVar6 = strerror(iVar1);
        FUN_140002d40(pcVar6, &local_78);
        goto LAB_1400045bc;
      case 0x6e:
        puVar21 = (uint *)*param_5;
        if (iVar20 == 5) {
          *(char *)puVar21 = (char)local_54;
        } else if (iVar20 == 1) {
          *(short *)puVar21 = (short)local_54;
        } else if ((iVar20 == 2) || (iVar20 != 3)) {
          *puVar21 = local_54;
        } else {
          *(longlong *)puVar21 = (longlong)(int)local_54;
        }
      LAB_1400049a0:
        puVar12 = param_5 + 1;
        goto LAB_1400045bc;
      case 0x70:
        if ((uVar10 == 0) && (local_70 == uVar19)) {
          auStack_68[0] = 0x10;
          local_70 = uVar19 | 0x200;
        }
        FUN_140002e30(0x78, *param_5, &local_78);
        puVar12 = param_5 + 1;
        goto LAB_1400045bc;
      case 0x73:
        if (iVar20 - 2U < 2) {
        LAB_140004d3a:
          puVar12 = param_5 + 1;
          _Str = (wchar_t *)*param_5;
          if (_Str == (wchar_t *)0x0) {
            _Str = L"(null)";
          }
          if ((int)auStack_68[0] < 0) {
            sVar9 = wcslen(_Str);
            FUN_140002a60((longlong)_Str, (int)sVar9, &local_78);
          } else {
            FUN_1400077a0((longlong)_Str, (longlong)(int)auStack_68[0]);
            FUN_140002a60((longlong)_Str, extraout_EAX, &local_78);
          }
        } else {
          FUN_140002d40((char *)*param_5, &local_78);
          puVar12 = param_5 + 1;
        }
        goto LAB_1400045bc;
      }
      pbVar17 = pbVar18;
      if (bVar3 == 0) {
        return local_54;
      }
    } while (true);
  }
  if (((local_70 & 0x4000) != 0) || ((int)local_54 < local_50)) {
    if ((local_70 & 0x2000) == 0) {
      *(char *)((longlong)&local_78->_ptr + (longlong)(int)local_54) =
          (char)uVar4;
    } else {
      fputc(uVar10, local_78);
    }
  }
  local_54 = uVar2 + 1;
  pbVar18 = pbVar16;
  puVar12 = param_5;
  goto LAB_1400045bc;
switchD_140004610_caseD_25:
  FUN_140002a00(0x25, &local_78);
LAB_1400045bc:
  bVar3 = *pbVar18;
  uVar4 = (uint)bVar3;
  pbVar16 = pbVar18 + 1;
  uVar10 = (uint)(char)bVar3;
  param_5 = puVar12;
  if (bVar3 == 0) {
    return local_54;
  }
  goto LAB_1400045ce;
}

int *FUN_140004fa0(int param_1)

{
  int iVar1;
  int *piVar2;
  int iVar3;

  iVar3 = 0;
  if (0x1b < param_1) {
    iVar1 = 4;
    do {
      iVar1 = iVar1 * 2;
      iVar3 = iVar3 + 1;
    } while (iVar1 + 0x17 < param_1);
  }
  piVar2 = (int *)FUN_140006c10(iVar3);
  *piVar2 = iVar3;
  return piVar2 + 1;
}

int *FUN_140004fe0(char *param_1, undefined8 *param_2, int param_3)

{
  char cVar1;
  int iVar2;
  int *piVar3;
  int *piVar4;
  char *pcVar5;
  int iVar6;

  if (param_3 < 0x1c) {
    iVar6 = 0;
  } else {
    iVar2 = 4;
    iVar6 = 0;
    do {
      iVar2 = iVar2 * 2;
      iVar6 = iVar6 + 1;
    } while (iVar2 + 0x17 < param_3);
  }
  piVar3 = (int *)FUN_140006c10(iVar6);
  pcVar5 = param_1 + 1;
  *piVar3 = iVar6;
  cVar1 = *param_1;
  *(char *)(piVar3 + 1) = cVar1;
  piVar4 = piVar3 + 1;
  while (cVar1 != '\0') {
    cVar1 = *pcVar5;
    piVar4 = (int *)((longlong)piVar4 + 1);
    pcVar5 = pcVar5 + 1;
    *(char *)piVar4 = cVar1;
  }
  if (param_2 != (undefined8 *)0x0) {
    *param_2 = piVar4;
  }
  return piVar3 + 1;
}

void FUN_140005060(longlong param_1)

{
  *(ulonglong *)(param_1 + 4) =
      CONCAT44(1 << ((byte) * (undefined4 *)(param_1 + -4) & 0x1f),
               *(undefined4 *)(param_1 + -4));
  FUN_140006d00((undefined8 *)(param_1 + -4));
  return;
}

int FUN_140005090(longlong param_1, longlong param_2)

{
  uint *puVar1;
  uint *puVar2;
  uint uVar3;
  int iVar4;
  ulonglong uVar5;
  longlong lVar6;
  uint *puVar7;
  ulonglong uVar8;
  uint *puVar9;
  ulonglong uVar10;
  int iVar11;
  uint *puVar12;
  uint *puVar13;
  ulonglong uVar14;

  if (*(int *)(param_1 + 0x14) < *(int *)(param_2 + 0x14)) {
    return 0;
  }
  iVar11 = *(int *)(param_2 + 0x14) + -1;
  puVar7 = (uint *)(param_2 + 0x18);
  puVar1 = (uint *)(param_1 + 0x18);
  puVar2 = puVar7 + iVar11;
  puVar9 = puVar1 + iVar11;
  uVar10 = (ulonglong)*puVar9 / (ulonglong)(*puVar2 + 1);
  iVar4 = (int)uVar10;
  if (*puVar2 + 1 <= *puVar9) {
    uVar14 = 0;
    uVar8 = 0;
    puVar12 = puVar1;
    puVar13 = puVar7;
    do {
      uVar3 = *puVar13;
      puVar13 = puVar13 + 1;
      uVar5 = uVar3 * uVar10 + uVar14;
      uVar14 = uVar5 >> 0x20;
      lVar6 = ((ulonglong)*puVar12 - (uVar5 & 0xffffffff)) - uVar8;
      *puVar12 = (uint)lVar6;
      uVar8 = (ulonglong)((uint)((ulonglong)lVar6 >> 0x20) & 1);
      puVar12 = puVar12 + 1;
    } while (puVar13 <= puVar2);
    if (*puVar9 == 0) {
      while ((puVar9 = puVar9 + -1, puVar1 < puVar9 && (*puVar9 == 0))) {
        iVar11 = iVar11 + -1;
      }
      *(int *)(param_1 + 0x14) = iVar11;
      uVar3 = FUN_1400072e0(param_1, param_2);
      goto joined_r0x000140005153;
    }
  }
  uVar3 = FUN_1400072e0(param_1, param_2);
joined_r0x000140005153:
  if (-1 < (int)uVar3) {
    uVar10 = 0;
    puVar9 = puVar1;
    do {
      uVar3 = *puVar7;
      puVar7 = puVar7 + 1;
      lVar6 = ((ulonglong)*puVar9 - (ulonglong)uVar3) - uVar10;
      *puVar9 = (uint)lVar6;
      uVar10 = (ulonglong)((uint)((ulonglong)lVar6 >> 0x20) & 1);
      puVar9 = puVar9 + 1;
    } while (puVar7 <= puVar2);
    puVar7 = puVar1 + iVar11;
    if (*puVar7 == 0) {
      while ((puVar7 = puVar7 + -1, puVar1 < puVar7 && (*puVar7 == 0))) {
        iVar11 = iVar11 + -1;
      }
      iVar4 = iVar4 + 1;
      *(int *)(param_1 + 0x14) = iVar11;
    } else {
      iVar4 = iVar4 + 1;
    }
  }
  return iVar4;
}

int *FUN_140005210(int *param_1, int param_2, uint *param_3, uint *param_4,
                   uint param_5, uint param_6, uint *param_7,
                   undefined8 *param_8)

{
  uint uVar1;
  bool bVar2;
  bool bVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  uint uVar7;
  undefined8 *puVar8;
  uint *puVar9;
  longlong lVar10;
  int *piVar11;
  byte *pbVar12;
  undefined8 *puVar13;
  undefined8 *puVar14;
  undefined8 *puVar15;
  undefined8 *puVar16;
  byte bVar17;
  int iVar18;
  int iVar19;
  uint uVar20;
  uint uVar21;
  char *pcVar22;
  bool bVar23;
  int iVar24;
  uint uVar25;
  uint *puVar26;
  byte *pbVar27;
  byte *pbVar28;
  bool bVar29;
  int iVar30;
  longlong lVar31;
  uint uVar32;
  uint uVar33;
  ulonglong uVar34;
  double dVar35;
  double dVar36;
  double dVar37;
  double dVar38;
  uint local_a8;
  uint uStack_a4;
  uint uStack_a0;
  uint uStack_88;
  uint uStack_60;
  uint auStack_4c[3];

  uVar25 = *param_4;
  local_a8 = param_6;
  *param_4 = uVar25 & 0xffffffcf;
  uVar4 = uVar25 & 7;
  if (uVar4 == 3) {
    iVar6 = 8;
    pcVar22 = "Infinity";
    *param_7 = 0xffff8000;
  } else {
    uVar7 = uVar25 & 4;
    if ((uVar25 & 4) == 0) {
      if (uVar4 != 0) {
        iVar6 = *param_1;
        iVar18 = 0;
        iVar24 = 0x20;
        if (0x20 < iVar6) {
          do {
            iVar30 = iVar24 * 2;
            iVar18 = iVar18 + 1;
            iVar19 = iVar24 * -2;
            iVar24 = iVar30;
          } while (iVar6 != iVar30 &&
                   SBORROW4(iVar6, iVar30) == iVar6 + iVar19 < 0);
        }
        puVar8 = (undefined8 *)FUN_140006c10(iVar18);
        lVar31 = (longlong)(iVar6 + -1 >> 5);
        puVar9 = param_3;
        puVar26 = (uint *)(puVar8 + 3);
        do {
          uVar4 = *puVar9;
          puVar9 = puVar9 + 1;
          *puVar26 = uVar4;
          puVar26 = puVar26 + 1;
        } while (puVar9 <= param_3 + lVar31);
        lVar10 = lVar31 * 4 + 4;
        if ((longlong)(param_3 + lVar31) + 1U < (longlong)param_3 + 1U) {
          lVar10 = 4;
        }
        lVar31 = lVar10 + (longlong)puVar8;
        uVar34 = lVar10 >> 2;
      LAB_14000531d:
        iVar24 = (int)uVar34;
        uVar4 = iVar24 - 1;
        uVar34 = (ulonglong)uVar4;
        if (*(int *)(lVar31 + 0x14) == 0)
          goto LAB_140005310;
        *(int *)((longlong)puVar8 + 0x14) = iVar24;
        puVar9 = (uint *)((longlong)puVar8 + (longlong)(int)uVar4 * 4 + 0x18);
        uVar4 = 0x1f;
        if (*puVar9 != 0) {
          for (; *puVar9 >> uVar4 == 0; uVar4 = uVar4 - 1) {
          }
        }
        iVar24 = iVar24 * 0x20 - (uVar4 ^ 0x1f);
        goto LAB_140005342;
      }
      goto LAB_1400054f0;
    }
    if (uVar4 != 4) {
      return (int *)0x0;
    }
    iVar6 = 3;
    pcVar22 = "NaN";
    *param_7 = 0xffff8000;
  }
  piVar11 = FUN_140004fe0(pcVar22, param_8, iVar6);
  return piVar11;
LAB_140005310:
  lVar31 = lVar31 + -4;
  if (uVar4 == 0)
    goto LAB_140005558;
  goto LAB_14000531d;
LAB_140006586:
  while (true) {
    pbVar28 = pbVar27 + 1;
    uVar4 = FUN_1400072e0((longlong)puVar15, (longlong)puVar13);
    if ((int)uVar4 < 1)
      break;
    *pbVar27 = (byte)uVar25;
    puVar16 = FUN_140006d70(puVar13, 10, 0);
    if (puVar14 == puVar13) {
      puVar14 = puVar16;
    }
    puVar8 = FUN_140006d70(puVar8, 10, 0);
    iVar6 = FUN_140005090((longlong)puVar8, (longlong)puVar15);
    uVar25 = iVar6 + 0x30;
    pbVar27 = pbVar28;
    puVar13 = puVar16;
  }
  if (uVar25 == 0x39) {
  LAB_140006911:
    *pbVar27 = 0x39;
    pbVar27 = pbVar28;
    goto LAB_140006049;
  }
  uVar25 = uVar25 + 1;
  uStack_a4 = 0x20;
LAB_1400065cc:
  *pbVar27 = (byte)uVar25;
  uVar7 = uStack_a4;
LAB_140005ed0:
  FUN_140006d00(puVar15);
  if (puVar13 == (undefined8 *)0x0)
    goto LAB_140005bd5;
  if ((puVar14 != (undefined8 *)0x0) && (puVar14 != puVar13)) {
    FUN_140006d00(puVar14);
  }
  goto LAB_140005bcd;
code_r0x000140005849:
  bVar17 = (char)uVar5 + 1;
LAB_14000584c:
  *pbVar27 = bVar17;
  uVar7 = 0x20;
  local_a8 = uStack_a4 + 1;
  goto LAB_140005bd5;
LAB_140005558:
  *(undefined4 *)((longlong)puVar8 + 0x14) = 0;
  iVar24 = 0;
LAB_140005342:
  auStack_4c[0] = FUN_140006aa0((longlong)puVar8);
  uStack_a0 = param_2;
  if (auStack_4c[0] != 0) {
    FUN_1400069a0((longlong)puVar8, auStack_4c[0]);
    uStack_a0 = param_2 + auStack_4c[0];
    iVar24 = iVar24 - auStack_4c[0];
  }
  if (*(int *)((longlong)puVar8 + 0x14) == 0) {
    FUN_140006d00(puVar8);
  LAB_1400054f0:
    *param_7 = 1;
    piVar11 = FUN_140004fe0("0", param_8, 1);
    return piVar11;
  }
  uVar34 = FUN_140007510((longlong)puVar8, (int *)auStack_4c);
  iVar30 = uStack_a0 + iVar24;
  iVar19 = iVar30 + -1;
  uVar4 = (uint)(uVar34 >> 0x20) & 0xfffff | 0x3ff00000;
  iVar18 = 1 - iVar30;
  if (-1 < iVar19) {
    iVar18 = iVar19;
  }
  dVar35 = ((double)(uVar34 & 0xffffffff | (ulonglong)uVar4 << 0x20) - 1.5) *
               0.289529654602168 +
           0.1760912590558 + (double)iVar19 * 0.301029995663981;
  if (0 < iVar18 + -0x435) {
    dVar35 = dVar35 + (double)(iVar18 + -0x435) * 7e-17;
  }
  uVar32 = (uint)dVar35;
  if ((dVar35 < 0.0) && ((double)(int)uVar32 != dVar35)) {
    uVar32 = uVar32 - 1;
  }
  dVar35 = (double)(uVar34 & 0xffffffff | (ulonglong)(uVar4 + iVar19 * 0x100000)
                                              << 0x20);
  iVar19 = iVar24 - iVar19;
  uVar4 = iVar19 - 1;
  if (uVar32 < 0x17) {
    if (dVar35 < (double)(&DAT_14000b1c0)[(int)uVar32]) {
      bVar2 = false;
      uVar32 = uVar32 - 1;
      goto LAB_140005598;
    }
    bVar2 = false;
    uVar20 = 0;
    if (iVar19 < 1) {
      uVar4 = 0;
      uVar20 = 1 - iVar19;
    }
  LAB_140005490:
    uVar4 = uVar4 + uVar32;
    uStack_88 = 0;
    uVar33 = uVar32;
  } else {
    bVar2 = true;
  LAB_140005598:
    uVar20 = 0;
    if ((int)uVar4 < 0) {
      uVar4 = 0;
      uVar20 = 1 - iVar19;
    }
    if (-1 < (int)uVar32)
      goto LAB_140005490;
    uVar20 = uVar20 - uVar32;
    uStack_88 = -uVar32;
    uVar33 = 0;
  }
  uVar21 = uStack_88;
  if (param_5 < 10) {
    if ((int)param_5 < 6) {
      bVar29 = iVar30 + 0x3fdU < 0x7f8;
      if (param_5 == 4) {
      LAB_140005caa:
        bVar3 = true;
      } else {
        if (param_5 == 5) {
        LAB_140006132:
          bVar3 = true;
          goto LAB_140005632;
        }
        bVar3 = false;
        if (param_5 != 2) {
          if (param_5 == 3)
            goto LAB_140005632;
          goto LAB_140005878;
        }
      }
    LAB_140005cb2:
      local_a8 = 1;
      auStack_4c[0] = local_a8;
      uStack_60 = local_a8;
      uVar1 = local_a8;
      if (0 < (int)param_6) {
        auStack_4c[0] = param_6;
        local_a8 = param_6;
        uStack_60 = param_6;
        uVar1 = param_6;
      }
    } else {
      bVar29 = false;
      param_5 = param_5 - 4;
      if (param_5 == 4)
        goto LAB_140005caa;
      if (param_5 == 5)
        goto LAB_140006132;
      bVar3 = false;
      if (param_5 == 2)
        goto LAB_140005cb2;
      param_5 = 3;
    LAB_140005632:
      uStack_60 = uVar32 + param_6;
      uVar1 = uStack_60 + 1;
      auStack_4c[0] = 1;
      if (0 < (int)uVar1) {
        auStack_4c[0] = uVar1;
      }
    }
    pbVar12 = (byte *)FUN_140004fa0(auStack_4c[0]);
    uVar5 = param_1[3] - 1;
    uStack_a4 = uVar5;
    if (uVar5 != 0) {
      uStack_a4 = 2;
      if (-1 < (int)uVar5) {
        uStack_a4 = uVar5;
      }
      if ((uVar25 & 8) == 0)
        goto LAB_1400058ea;
      uStack_a4 = 3 - uStack_a4;
    }
    bVar29 = (bool)(uVar1 < 0xf & bVar29);
    if ((!bVar29) || (uVar32 != 0 || uStack_a4 != 0))
      goto LAB_1400058ea;
    auStack_4c[0] = 0;
    if ((bVar2) && (dVar35 < 1.0)) {
      if (uVar1 == 0) {
        dVar38 = dVar35 + dVar35 + 7.0;
        dVar38 =
            (double)((ulonglong)dVar38 & 0xffffffff |
                     (ulonglong)((int)((ulonglong)dVar38 >> 0x20) + 0xfcc00000)
                         << 0x20);
        goto LAB_14000632b;
      }
      if (0 < (int)uStack_60) {
        dVar36 = dVar35 * 10.0;
        uStack_a4 = 0xffffffff;
        dVar38 = dVar36 * 3.0 + 7.0;
        dVar38 =
            (double)((ulonglong)dVar38 & 0xffffffff |
                     (ulonglong)((int)((ulonglong)dVar38 >> 0x20) + 0xfcc00000)
                         << 0x20);
        uVar25 = uStack_60;
        goto LAB_14000575f;
      }
    LAB_140006354:
      uStack_a4 = 0;
      goto LAB_1400058ea;
    }
    dVar38 = dVar35 + dVar35 + 7.0;
    dVar38 = (double)((ulonglong)dVar38 & 0xffffffff |
                      (ulonglong)((int)((ulonglong)dVar38 >> 0x20) + 0xfcc00000)
                          << 0x20);
    if (uVar1 == 0) {
    LAB_14000632b:
      if (dVar38 < dVar35 - 5.0) {
        local_a8 = 2;
        puVar15 = (undefined8 *)0x0;
        puVar13 = (undefined8 *)0x0;
        goto LAB_140005bb1;
      }
      if (-dVar38 <= dVar35 - 5.0)
        goto LAB_140006354;
      goto LAB_140005cd6;
    }
    uStack_a4 = 0;
    uVar25 = uVar1;
    dVar36 = dVar35;
  LAB_14000575f:
    if (bVar3) {
      pbVar28 = pbVar12 + 1;
      dVar38 = 0.5 / (double)(&DAT_14000b1c0)[(int)(uVar25 - 1)] - dVar38;
      *pbVar12 = (char)(int)dVar36 + 0x30;
      dVar36 = dVar36 - (double)(int)dVar36;
      pbVar27 = pbVar28;
      if (dVar38 <= dVar36) {
        do {
          if (1.0 - dVar36 < dVar38) {
            uVar5 = (uint)pbVar27[-1];
            pbVar28 = pbVar27;
            goto LAB_140005840;
          }
          auStack_4c[0] = auStack_4c[0] + 1;
          if ((int)uVar25 <= (int)auStack_4c[0])
            goto LAB_140006354;
          pbVar28 = pbVar27 + 1;
          dVar38 = dVar38 * 10.0;
          iVar18 = (int)(dVar36 * 10.0);
          *pbVar27 = (char)iVar18 + 0x30;
          dVar36 = dVar36 * 10.0 - (double)iVar18;
          pbVar27 = pbVar28;
        } while (dVar38 <= dVar36);
      }
      uVar7 = (uint)NAN(dVar36);
      if (dVar36 != 0.0) {
        uVar7 = 1;
      }
      uVar7 = uVar7 << 4;
      local_a8 = uStack_a4 + 1;
      goto LAB_140005bd5;
    }
    dVar38 = (double)(&DAT_14000b1c0)[(int)(uVar25 - 1)] * dVar38;
    auStack_4c[0] = 1;
    pbVar27 = pbVar12;
    dVar37 = dVar36;
    bVar23 = false;
    while (true) {
      iVar6 = (int)dVar37;
      if (iVar6 != 0) {
        dVar37 = dVar37 - (double)iVar6;
        bVar23 = bVar29;
      }
      uVar5 = iVar6 + 0x30;
      pbVar28 = pbVar27 + 1;
      *pbVar27 = (byte)uVar5;
      if (auStack_4c[0] == uVar25)
        break;
      dVar37 = dVar37 * 10.0;
      auStack_4c[0] = auStack_4c[0] + 1;
      pbVar27 = pbVar28;
      bVar23 = bVar29;
    }
    if (!bVar23) {
      dVar37 = dVar36;
    }
    if (dVar38 + 0.5 < dVar37) {
    LAB_140005840:
      do {
        pbVar27 = pbVar28 + -1;
        if ((char)uVar5 != '9')
          goto code_r0x000140005849;
        if (pbVar27 == pbVar12) {
          uStack_a4 = uStack_a4 + 1;
          bVar17 = 0x31;
          goto LAB_14000584c;
        }
        uVar5 = (uint)pbVar28[-2];
        pbVar28 = pbVar27;
      } while (true);
    }
    if (dVar37 < 0.5 - dVar38) {
      uVar7 = (uint)NAN(dVar37);
      if (dVar37 != 0.0) {
        uVar7 = 1;
      }
      uVar7 = uVar7 << 4;
      local_a8 = uStack_a4 + 1;
      goto LAB_140005bd5;
    }
    if (((int)uStack_a0 < 0) || (param_1[5] < 0)) {
      uStack_a4 = 0;
      puVar13 = (undefined8 *)0x0;
      uStack_a0 = uVar20;
      goto LAB_140005a12;
    }
    dVar38 = 1.0;
    if (((int)local_a8 < 0) && ((int)uVar1 < 1))
      goto LAB_140005929;
    uStack_a4 = 0;
  LAB_14000621a:
    auStack_4c[0] = 1;
    local_a8 = uVar32 + 1;
    uVar25 = (uint)(dVar35 / dVar38);
    *pbVar12 = (char)uVar25 + 0x30;
    pbVar27 = pbVar12;
    for (dVar35 = dVar35 - (double)(int)uVar25 * dVar38;
         pbVar28 = pbVar27 + 1, dVar35 != 0.0;
         dVar35 = dVar35 * 10.0 - (double)(int)uVar25 * dVar38) {
      if (auStack_4c[0] == uVar1) {
        if (uStack_a4 == 0) {
          if ((dVar38 < dVar35 + dVar35) ||
              ((dVar35 + dVar35 == dVar38 && ((uVar25 & 1) != 0))))
            goto LAB_140006798;
        } else if (uStack_a4 == 1) {
        LAB_140006798:
          uVar5 = (uint)*pbVar27;
          uStack_a4 = uVar32;
          goto LAB_140005840;
        }
        uVar7 = 0x10;
        break;
      }
      auStack_4c[0] = auStack_4c[0] + 1;
      uVar25 = (uint)((dVar35 * 10.0) / dVar38);
      *pbVar28 = (char)uVar25 + 0x30;
      pbVar27 = pbVar28;
    }
    goto LAB_140005bd5;
  }
  param_5 = 0;
LAB_140005878:
  auStack_4c[0] = (int)((double)iVar6 * 0.30103) + 3;
  pbVar12 = (byte *)FUN_140004fa0(auStack_4c[0]);
  local_a8 = 0;
  uStack_a4 = 0;
  bVar3 = true;
  uStack_60 = 0xffffffff;
  uVar1 = 0xffffffff;
LAB_1400058ea:
  if (((int)uStack_a0 < 0) || (param_1[5] < (int)uVar32)) {
    if (bVar3) {
      auStack_4c[0] = (iVar6 - iVar24) + 1;
      if ((int)(uStack_a0 - (iVar6 - iVar24)) < param_1[1]) {
        if ((param_5 - 3 & 0xfffffffd) == 0) {
        LAB_1400060f3:
          if ((int)(uVar1 - 1) <= (int)uStack_88) {
            uVar21 = uStack_88 - (uVar1 - 1);
            if ((int)uVar1 < 0) {
              auStack_4c[0] = 0;
              uVar25 = uVar20;
              uStack_a0 = uVar20 - uVar1;
            } else {
              uVar4 = uVar4 + uVar1;
              auStack_4c[0] = uVar1;
              uVar25 = uVar1 + uVar20;
              uStack_a0 = uVar20;
            }
            goto LAB_1400059e5;
          }
        } else {
          auStack_4c[0] = (uStack_a0 - param_1[1]) + 1;
          if (((int)param_5 < 2 || (int)uVar1 < 1) ||
              ((int)auStack_4c[0] <= (int)uVar1))
            goto LAB_1400059cf;
          if ((int)(uVar1 - 1) <= (int)uStack_88) {
            uVar21 = uStack_88 - (uVar1 - 1);
            uVar4 = uVar4 + uVar1;
            auStack_4c[0] = uVar1;
            uVar25 = uVar1 + uVar20;
            uStack_a0 = uVar20;
            goto LAB_1400059e5;
          }
        }
        uVar21 = 0;
        uVar33 = uVar33 + ((uVar1 - 1) - uStack_88);
        uVar4 = uVar4 + uVar1;
        auStack_4c[0] = uVar1;
        uStack_88 = uVar1 - 1;
        uVar25 = uVar1 + uVar20;
        uStack_a0 = uVar20;
      } else {
        if (1 < (int)param_5)
          goto LAB_1400060f3;
      LAB_1400059cf:
        uVar4 = uVar4 + auStack_4c[0];
        uVar25 = auStack_4c[0] + uVar20;
        uStack_a0 = uVar20;
      }
    LAB_1400059e5:
      uVar20 = uVar25;
      puVar13 = (undefined8 *)FUN_140006e30(1);
    } else {
      puVar13 = (undefined8 *)0x0;
      uStack_a0 = uVar20;
    }
  LAB_140005a12:
    if ((0 < (int)uStack_a0) && (0 < (int)uVar4)) {
      auStack_4c[0] = uStack_a0;
      if ((int)uVar4 < (int)uStack_a0) {
        auStack_4c[0] = uVar4;
      }
      uVar20 = uVar20 - auStack_4c[0];
      uStack_a0 = uStack_a0 - auStack_4c[0];
      uVar4 = uVar4 - auStack_4c[0];
    }
    puVar14 = puVar8;
    if (uStack_88 != 0) {
      if (bVar3) {
        if (uVar21 != 0) {
          puVar13 = FUN_140007050(puVar13, uVar21);
          puVar14 =
              (undefined8 *)FUN_140006ef0((longlong)puVar13, (longlong)puVar8);
          FUN_140006d00(puVar8);
          uStack_88 = uStack_88 - uVar21;
          if (uStack_88 == 0)
            goto LAB_140005a90;
        }
        puVar14 = FUN_140007050(puVar14, uStack_88);
      } else {
        puVar14 = FUN_140007050(puVar8, uStack_88);
      }
    }
  LAB_140005a90:
    puVar15 = (undefined8 *)FUN_140006e30(1);
    if (uVar33 == 0) {
      bVar29 = false;
      if ((((int)param_5 < 2) && (iVar24 == 1)) && (param_1[1] + 1 < param_2)) {
        uVar20 = uVar20 + 1;
        uVar4 = uVar4 + 1;
        bVar29 = true;
      }
      uVar25 = 0x1f;
    } else {
      puVar15 = FUN_140007050(puVar15, uVar33);
      if ((((int)param_5 < 2) && (iVar24 == 1)) && (param_1[1] + 1 < param_2)) {
        uVar20 = uVar20 + 1;
        uVar4 = uVar4 + 1;
        bVar29 = true;
      } else {
        bVar29 = false;
      }
      puVar9 =
          (uint *)((longlong)puVar15 +
                   (longlong)(*(int *)((longlong)puVar15 + 0x14) + -1) * 4 +
                   0x18);
      uVar25 = 0x1f;
      if (*puVar9 != 0) {
        for (; *puVar9 >> uVar25 == 0; uVar25 = uVar25 - 1) {
        }
      }
      uVar25 = uVar25 ^ 0x1f;
    }
    uVar25 = (uVar25 - uVar4) - 4 & 0x1f;
    puVar8 = puVar14;
    auStack_4c[0] = uVar25;
    if (0 < (int)(uVar20 + uVar25)) {
      puVar8 = (undefined8 *)FUN_1400071d0(puVar14, uVar20 + uVar25);
    }
    if (0 < (int)(auStack_4c[0] + uVar4)) {
      puVar15 = (undefined8 *)FUN_1400071d0(puVar15, auStack_4c[0] + uVar4);
    }
    bVar23 = (int)param_5 < 3;
    if ((bVar2) && (uVar4 = FUN_1400072e0((longlong)puVar8, (longlong)puVar15),
                    (int)uVar4 < 0)) {
      uVar4 = uVar32 - 1;
      puVar8 = FUN_140006d70(puVar8, 10, 0);
      if (bVar3) {
        puVar13 = FUN_140006d70(puVar13, 10, 0);
        uVar20 = uVar32;
        if (bVar23 || 0 < (int)uStack_60) {
        LAB_140005d0f:
          local_a8 = uVar20;
          puVar14 = puVar13;
          if (0 < (int)(uStack_a0 + uVar25)) {
            puVar14 = (undefined8 *)FUN_1400071d0(puVar13, uStack_a0 + uVar25);
          }
          puVar13 = puVar14;
          if (bVar29) {
            puVar13 = (undefined8 *)FUN_140006c10(*(int *)(puVar14 + 1));
            memcpy(puVar13 + 2, puVar14 + 2,
                   (longlong) * (int *)((longlong)puVar14 + 0x14) * 4 + 8);
            puVar13 = (undefined8 *)FUN_1400071d0(puVar13, 1);
          }
          auStack_4c[0] = 1;
          pbVar27 = pbVar12;
          while (true) {
            iVar6 = FUN_140005090((longlong)puVar8, (longlong)puVar15);
            uVar25 = iVar6 + 0x30;
            uVar4 = FUN_1400072e0((longlong)puVar8, (longlong)puVar14);
            puVar16 = (undefined8 *)FUN_140007330((longlong)puVar15,
                                                  (longlong)puVar13);
            if (*(int *)(puVar16 + 2) == 0) {
              uVar32 = FUN_1400072e0((longlong)puVar8, (longlong)puVar16);
              FUN_140006d00(puVar16);
              if ((uVar32 == 0 && param_5 == 0) &&
                  (uVar32 = 0, (*param_3 & 1) == 0 && uStack_a4 == 0)) {
                if (uVar25 == 0x39) {
                  pbVar28 = pbVar27 + 1;
                  goto LAB_140006911;
                }
                if ((int)uVar4 < 1) {
                  uVar7 = 0x10;
                  if (*(int *)((longlong)puVar8 + 0x14) < 2) {
                    uVar7 = (uint)(*(int *)(puVar8 + 3) != 0) << 4;
                  }
                } else {
                  uVar7 = 0x20;
                  uVar25 = iVar6 + 0x31;
                }
                *pbVar27 = (byte)uVar25;
                pbVar28 = pbVar27 + 1;
                goto LAB_140005ed0;
              }
            } else {
              FUN_140006d00(puVar16);
              uVar32 = 1;
            }
            if (((int)uVar4 < 0) ||
                ((uVar4 == 0 && param_5 == 0 && ((*param_3 & 1) == 0))))
              break;
            pbVar28 = pbVar27 + 1;
            if ((0 < (int)uVar32) && (uStack_a4 != 2)) {
              if (uVar25 == 0x39)
                goto LAB_140006911;
              *pbVar27 = (char)iVar6 + 0x31;
              uVar7 = 0x20;
              goto LAB_140005ed0;
            }
            *pbVar27 = (byte)uVar25;
            if (auStack_4c[0] == uStack_60)
              goto LAB_140006002;
            puVar8 = FUN_140006d70(puVar8, 10, 0);
            if (puVar14 == puVar13) {
              puVar14 = FUN_140006d70(puVar14, 10, 0);
              puVar13 = puVar14;
            } else {
              puVar14 = FUN_140006d70(puVar14, 10, 0);
              puVar13 = FUN_140006d70(puVar13, 10, 0);
            }
            auStack_4c[0] = auStack_4c[0] + 1;
            pbVar27 = pbVar28;
          }
          if (uStack_a4 == 0) {
            if (0 < (int)uVar32)
              goto LAB_1400066fb;
          } else {
            if ((1 < *(int *)((longlong)puVar8 + 0x14)) ||
                (*(int *)(puVar8 + 3) != 0)) {
              if (uStack_a4 != 2)
                goto LAB_140006586;
              goto LAB_14000675e;
            }
            if ((int)uVar32 < 1) {
              pbVar28 = pbVar27 + 1;
              uStack_a4 = uVar7;
              goto LAB_1400065cc;
            }
          LAB_1400066fb:
            puVar8 = (undefined8 *)FUN_1400071d0(puVar8, 1);
            uVar4 = FUN_1400072e0((longlong)puVar8, (longlong)puVar15);
            if (((int)uVar4 < 1) && ((uVar4 != 0 || ((uVar25 & 1) == 0)))) {
              uStack_a4 = 0x20;
              goto LAB_140006754;
            }
            if (uVar25 == 0x39) {
              pbVar28 = pbVar27 + 1;
              goto LAB_140006911;
            }
            uStack_a4 = 0x20;
            uVar25 = iVar6 + 0x31;
          }
        LAB_140006754:
          if (*(int *)((longlong)puVar8 + 0x14) < 2) {
            if (*(int *)(puVar8 + 3) == 0) {
              pbVar28 = pbVar27 + 1;
            } else {
              uStack_a4 = 0x10;
              pbVar28 = pbVar27 + 1;
            }
            goto LAB_1400065cc;
          }
        LAB_14000675e:
          pbVar28 = pbVar27 + 1;
          uStack_a4 = 0x10;
          goto LAB_1400065cc;
        }
      } else if (bVar23 || 0 < (int)uStack_60)
        goto LAB_140005fa0;
    } else {
      uStack_60 = uVar1;
      if ((0 < (int)uVar1) || (uVar4 = uVar32, bVar23)) {
        uVar20 = uVar32 + 1;
        uVar32 = uVar32 + 1;
        if (bVar3)
          goto LAB_140005d0f;
      LAB_140005fa0:
        local_a8 = uVar32;
        auStack_4c[0] = 1;
        pbVar27 = pbVar12;
        while (true) {
          pbVar28 = pbVar27 + 1;
          iVar6 = FUN_140005090((longlong)puVar8, (longlong)puVar15);
          uVar25 = iVar6 + 0x30;
          *pbVar27 = (byte)uVar25;
          if ((int)uStack_60 <= (int)auStack_4c[0])
            break;
          puVar8 = FUN_140006d70(puVar8, 10, 0);
          auStack_4c[0] = auStack_4c[0] + 1;
          pbVar27 = pbVar28;
        }
        puVar14 = (undefined8 *)0x0;
      LAB_140006002:
        if (uStack_a4 == 0) {
          puVar8 = (undefined8 *)FUN_1400071d0(puVar8, 1);
          uVar4 = FUN_1400072e0((longlong)puVar8, (longlong)puVar15);
          pbVar27 = pbVar28;
          if ((0 < (int)uVar4) || ((uVar4 == 0 && ((uVar25 & 1) != 0)))) {
          LAB_140006049:
            do {
              pbVar28 = pbVar27;
              pbVar27 = pbVar28 + -1;
              if (pbVar28[-1] != 0x39) {
                *pbVar27 = pbVar28[-1] + 1;
                uVar7 = 0x20;
                goto LAB_140005ed0;
              }
            } while (pbVar27 != pbVar12);
            local_a8 = local_a8 + 1;
            *pbVar12 = 0x31;
            uVar7 = 0x20;
            goto LAB_140005ed0;
          }
        LAB_1400064ce:
          uVar7 = 0x10;
          if (1 < *(int *)((longlong)puVar8 + 0x14))
            goto LAB_140005ed0;
          iVar6 = *(int *)(puVar8 + 3);
        } else {
          if (uStack_a4 == 2)
            goto LAB_1400064ce;
          pbVar27 = pbVar28;
          if ((1 < *(int *)((longlong)puVar8 + 0x14)) ||
              (iVar6 = *(int *)(puVar8 + 3), iVar6 != 0))
            goto LAB_140006049;
        }
        uVar7 = (uint)(iVar6 != 0) << 4;
        goto LAB_140005ed0;
      }
    }
    if (uStack_60 != 0)
      goto LAB_140005cdb;
    puVar15 = FUN_140006d70(puVar15, 5, 0);
    uVar25 = FUN_1400072e0((longlong)puVar8, (longlong)puVar15);
    if ((int)uVar25 < 1)
      goto LAB_140005cdb;
    local_a8 = uVar4 + 2;
  LAB_140005bb1:
    *pbVar12 = 0x31;
    uVar7 = 0x20;
    pbVar28 = pbVar12 + 1;
  } else {
    dVar38 = (double)(&DAT_14000b1c0)[(int)uVar32];
    if ((-1 < (int)local_a8) || (0 < (int)uVar1))
      goto LAB_14000621a;
    if (uVar1 == 0) {
    LAB_140005929:
      if (dVar38 * 5.0 < dVar35) {
        puVar15 = (undefined8 *)0x0;
        puVar13 = (undefined8 *)0x0;
        local_a8 = uVar32 + 2;
        goto LAB_140005bb1;
      }
    }
  LAB_140005cd6:
    puVar15 = (undefined8 *)0x0;
    puVar13 = (undefined8 *)0x0;
  LAB_140005cdb:
    uVar7 = 0x10;
    local_a8 = -local_a8;
    pbVar28 = pbVar12;
  }
  FUN_140006d00(puVar15);
  if (puVar13 == (undefined8 *)0x0)
    goto LAB_140005bd5;
LAB_140005bcd:
  FUN_140006d00(puVar13);
LAB_140005bd5:
  if (pbVar12 < pbVar28) {
    do {
      if (pbVar28[-1] != 0x30)
        break;
      pbVar28 = pbVar28 + -1;
    } while (pbVar28 != pbVar12);
  }
  FUN_140006d00(puVar8);
  *pbVar28 = 0;
  *param_7 = local_a8;
  if (param_8 != (undefined8 *)0x0) {
    *param_8 = pbVar28;
  }
  *param_4 = *param_4 | uVar7;
  return (int *)pbVar12;
}

void FUN_1400069a0(longlong param_1, uint param_2)

{
  uint *puVar1;
  uint *puVar2;
  uint uVar3;
  sbyte sVar4;
  int iVar5;
  uint *puVar6;
  longlong lVar7;
  longlong lVar8;
  uint *puVar9;
  uint *puVar10;
  uint uVar11;

  lVar7 = (longlong) * (int *)(param_1 + 0x14);
  if ((int)param_2 >> 5 < *(int *)(param_1 + 0x14)) {
    puVar1 = (uint *)(param_1 + 0x18);
    lVar8 = (longlong)((int)param_2 >> 5);
    puVar2 = puVar1 + lVar7;
    puVar6 = puVar1 + lVar8;
    if ((param_2 & 0x1f) == 0) {
      puVar9 = puVar1;
      if (puVar2 <= puVar6)
        goto LAB_1400069b6;
      do {
        puVar10 = puVar6 + 1;
        *puVar9 = *puVar6;
        puVar6 = puVar10;
        puVar9 = puVar9 + 1;
      } while (puVar10 < puVar2);
      puVar6 = puVar1 + (lVar7 - lVar8);
    } else {
      uVar3 = *puVar6;
      puVar6 = puVar6 + 1;
      sVar4 = (sbyte)(param_2 & 0x1f);
      uVar11 = uVar3 >> sVar4;
      puVar9 = puVar1;
      if (puVar6 < puVar2) {
        do {
          puVar10 = puVar6 + 1;
          *puVar9 = *puVar6 << (0x20U - sVar4 & 0x1f) | uVar11;
          uVar3 = *puVar6;
          uVar11 = uVar3 >> sVar4;
          puVar9 = puVar9 + 1;
          puVar6 = puVar10;
        } while (puVar10 < puVar2);
        puVar6 = (uint *)(param_1 + 0x14 + (lVar7 - lVar8) * 4);
        *puVar6 = uVar11;
        if (uVar3 >> sVar4 == 0)
          goto LAB_140006a65;
      } else {
        *(uint *)(param_1 + 0x18) = uVar11;
        puVar6 = puVar1;
        if (uVar3 >> sVar4 == 0)
          goto LAB_1400069b6;
      }
      puVar6 = puVar6 + 1;
    }
  LAB_140006a65:
    iVar5 = (int)((longlong)puVar6 - (longlong)puVar1 >> 2);
    *(int *)(param_1 + 0x14) = iVar5;
    if (iVar5 != 0) {
      return;
    }
  } else {
  LAB_1400069b6:
    *(undefined4 *)(param_1 + 0x14) = 0;
  }
  *(undefined4 *)(param_1 + 0x18) = 0;
  return;
}

int FUN_140006aa0(longlong param_1)

{
  uint *puVar1;
  uint uVar2;
  int iVar3;
  uint *puVar4;
  int iVar5;

  puVar4 = (uint *)(param_1 + 0x18);
  puVar1 = puVar4 + *(int *)(param_1 + 0x14);
  iVar5 = 0;
  while (true) {
    if (puVar1 <= puVar4) {
      return iVar5;
    }
    if (*puVar4 != 0)
      break;
    puVar4 = puVar4 + 1;
    iVar5 = iVar5 + 0x20;
  }
  if (puVar1 <= puVar4) {
    return iVar5;
  }
  iVar3 = 0;
  for (uVar2 = *puVar4; (uVar2 & 1) == 0; uVar2 = uVar2 >> 1 | 0x80000000) {
    iVar3 = iVar3 + 1;
  }
  return iVar5 + iVar3;
}

// WARNING: Removing unreachable block (ram,0x000140006bab)
// WARNING: Removing unreachable block (ram,0x000140006b90)
// WARNING: Removing unreachable block (ram,0x000140006b9c)

void FUN_140006ae0(int param_1)

{
  if (DAT_14000eaf0 != 2) {
    if (DAT_14000eaf0 != 0) {
      if (DAT_14000eaf0 == 1) {
        do {
          Sleep(1);
        } while (DAT_14000eaf0 == 1);
        if (DAT_14000eaf0 == 2)
          goto LAB_140006b76;
      }
      return;
    }
    LOCK();
    DAT_14000eaf0 = 1;
    UNLOCK();
    InitializeCriticalSection((LPCRITICAL_SECTION)&DAT_14000eb00);
    InitializeCriticalSection((LPCRITICAL_SECTION)&DAT_14000eb28);
    FUN_140001410((_onexit_t)&LAB_140006bc0);
    DAT_14000eaf0 = 2;
  }
LAB_140006b76:
  // WARNING: Could not recover jumptable at 0x000140006b89. Too many branches
  // WARNING: Treating indirect jump as call
  EnterCriticalSection(
      (LPCRITICAL_SECTION)(&DAT_14000eb00 + (-param_1 & 0x28)));
  return;
}

void FUN_140006c10(int param_1)

{
  int iVar1;
  undefined8 *puVar2;
  ulonglong uVar3;
  int iVar4;

  FUN_140006ae0(0);
  iVar1 = DAT_14000eaf0;
  if (param_1 < 10) {
    puVar2 = *(undefined8 **)(&DAT_14000eaa0 + (longlong)param_1 * 8);
    if (puVar2 != (undefined8 *)0x0) {
      *(undefined8 *)(&DAT_14000eaa0 + (longlong)param_1 * 8) = *puVar2;
      goto joined_r0x000140006c97;
    }
    iVar4 = 1 << ((byte)param_1 & 0x1f);
    uVar3 = (longlong)(iVar4 + -1) * 4 + 0x27U >> 3;
    if (0x120 < ((longlong)(PTR_DAT_140009060 + -0x14000e1a0) >> 3) + uVar3)
      goto LAB_140006c7c;
    puVar2 = (undefined8 *)PTR_DAT_140009060;
    PTR_DAT_140009060 = PTR_DAT_140009060 + uVar3 * 8;
  } else {
    iVar4 = 1 << ((byte)param_1 & 0x1f);
    uVar3 = (longlong)(iVar4 + -1) * 4 + 0x27U >> 3 & 0xffffffff;
  LAB_140006c7c:
    puVar2 = (undefined8 *)malloc(uVar3 << 3);
    if (puVar2 == (undefined8 *)0x0) {
      return;
    }
  }
  iVar1 = DAT_14000eaf0;
  *(int *)(puVar2 + 1) = param_1;
  *(int *)((longlong)puVar2 + 0xc) = iVar4;
joined_r0x000140006c97:
  if (iVar1 == 2) {
    LeaveCriticalSection((LPCRITICAL_SECTION)&DAT_14000eb00);
  }
  puVar2[2] = 0;
  return;
}

void FUN_140006d00(undefined8 *param_1)

{
  undefined8 uVar1;
  bool bVar2;

  if (param_1 != (undefined8 *)0x0) {
    if (9 < *(int *)(param_1 + 1)) {
      free(param_1);
      return;
    }
    FUN_140006ae0(0);
    bVar2 = DAT_14000eaf0 == 2;
    uVar1 =
        *(undefined8 *)(&DAT_14000eaa0 + (longlong) * (int *)(param_1 + 1) * 8);
    *(undefined8 **)(&DAT_14000eaa0 + (longlong) * (int *)(param_1 + 1) * 8) =
        param_1;
    *param_1 = uVar1;
    if (bVar2) {
      // WARNING: Could not recover jumptable at 0x000140006d5c. Too many
      // branches WARNING: Treating indirect jump as call
      LeaveCriticalSection((LPCRITICAL_SECTION)&DAT_14000eb00);
      return;
    }
  }
  return;
}

undefined8 *FUN_140006d70(undefined8 *param_1, int param_2, int param_3)

{
  int iVar1;
  ulonglong uVar2;
  undefined8 *puVar3;
  longlong lVar4;
  undefined4 uVar5;
  ulonglong uVar6;

  iVar1 = *(int *)((longlong)param_1 + 0x14);
  uVar6 = (ulonglong)param_3;
  lVar4 = 0;
  do {
    uVar2 = (ulonglong) * (uint *)((longlong)param_1 + lVar4 * 4 + 0x18) *
                (longlong)param_2 +
            uVar6;
    *(int *)((longlong)param_1 + lVar4 * 4 + 0x18) = (int)uVar2;
    lVar4 = lVar4 + 1;
    uVar6 = uVar2 >> 0x20;
  } while ((int)lVar4 < iVar1);
  puVar3 = param_1;
  if (uVar6 != 0) {
    uVar5 = (undefined4)(uVar2 >> 0x20);
    if (iVar1 < *(int *)((longlong)param_1 + 0xc)) {
      *(undefined4 *)((longlong)param_1 + (longlong)iVar1 * 4 + 0x18) = uVar5;
      *(int *)((longlong)param_1 + 0x14) = iVar1 + 1;
    } else {
      puVar3 = (undefined8 *)FUN_140006c10(*(int *)(param_1 + 1) + 1);
      if (puVar3 != (undefined8 *)0x0) {
        memcpy(puVar3 + 2, param_1 + 2,
               (longlong) * (int *)((longlong)param_1 + 0x14) * 4 + 8);
        FUN_140006d00(param_1);
        *(undefined4 *)((longlong)puVar3 + (longlong)iVar1 * 4 + 0x18) = uVar5;
        *(int *)((longlong)puVar3 + 0x14) = iVar1 + 1;
      }
    }
  }
  return puVar3;
}

void FUN_140006e30(undefined4 param_1)

{
  int iVar1;
  undefined8 *puVar2;

  FUN_140006ae0(0);
  if (DAT_14000eaa8 == (undefined8 *)0x0) {
    if (((longlong)(PTR_DAT_140009060 + -0x14000e1a0) >> 3) + 5U < 0x121) {
      puVar2 = (undefined8 *)PTR_DAT_140009060;
      PTR_DAT_140009060 = PTR_DAT_140009060 + 0x28;
    } else {
      puVar2 = (undefined8 *)malloc(0x28);
      if (puVar2 == (undefined8 *)0x0) {
        return;
      }
    }
    iVar1 = DAT_14000eaf0;
    puVar2[1] = 0x200000001;
  } else {
    puVar2 = DAT_14000eaa8;
    DAT_14000eaa8 = (undefined8 *)*DAT_14000eaa8;
    iVar1 = DAT_14000eaf0;
  }
  if (iVar1 == 2) {
    LeaveCriticalSection((LPCRITICAL_SECTION)&DAT_14000eb00);
  }
  *(undefined4 *)(puVar2 + 3) = param_1;
  puVar2[2] = 0x100000000;
  return;
}

longlong FUN_140006ef0(longlong param_1, longlong param_2)

{
  uint *puVar1;
  uint *puVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  longlong lVar7;
  uint *puVar8;
  ulonglong uVar9;
  int iVar10;
  uint *puVar11;
  uint *puVar12;
  int iVar13;
  uint *puVar14;
  ulonglong uVar15;
  uint *puVar16;
  longlong lVar17;

  iVar3 = *(int *)(param_1 + 0x14);
  iVar10 = *(int *)(param_2 + 0x14);
  lVar17 = param_1;
  iVar4 = iVar10;
  if (iVar10 <= iVar3) {
    lVar17 = param_2;
    param_2 = param_1;
    iVar4 = iVar3;
    iVar3 = iVar10;
  }
  iVar10 = *(int *)(param_2 + 8);
  iVar13 = iVar4 + iVar3;
  if (*(int *)(param_2 + 0xc) < iVar13) {
    iVar10 = iVar10 + 1;
  }
  lVar7 = FUN_140006c10(iVar10);
  if (lVar7 != 0) {
    puVar8 = (uint *)(lVar7 + 0x18);
    puVar14 = puVar8 + iVar13;
    if (puVar8 < puVar14) {
      puVar8 = (uint *)memset(
          puVar8, 0,
          ((longlong)puVar14 + (-0x19 - lVar7) & 0xfffffffffffffffcU) + 4);
    }
    puVar16 = (uint *)(lVar17 + 0x18);
    puVar1 = puVar16 + iVar3;
    puVar2 = (uint *)(param_2 + 0x18) + iVar4;
    if (puVar16 < puVar1) {
      lVar17 = ((longlong)puVar2 + (-0x19 - param_2) & 0xfffffffffffffffcU) + 4;
      if (puVar2 < (uint *)(param_2 + 0x19)) {
        lVar17 = 4;
      }
      do {
        while (true) {
          uVar5 = *puVar16;
          puVar16 = puVar16 + 1;
          if (uVar5 == 0)
            break;
          uVar15 = 0;
          puVar11 = puVar8;
          puVar12 = (uint *)(param_2 + 0x18);
          do {
            uVar6 = *puVar12;
            puVar12 = puVar12 + 1;
            uVar9 = (ulonglong)uVar6 * (ulonglong)uVar5 + (ulonglong)*puVar11 +
                    uVar15;
            *puVar11 = (uint)uVar9;
            uVar15 = uVar9 >> 0x20;
            puVar11 = puVar11 + 1;
          } while (puVar12 < puVar2);
          *(int *)((longlong)puVar8 + lVar17) = (int)(uVar9 >> 0x20);
          puVar8 = puVar8 + 1;
          if (puVar1 <= puVar16)
            goto LAB_140007013;
        }
        puVar8 = puVar8 + 1;
      } while (puVar16 < puVar1);
    }
  LAB_140007013:
    if (0 < iVar13) {
      do {
        puVar8 = puVar14 + -1;
        puVar14 = puVar14 + -1;
        if (*puVar8 != 0)
          break;
        iVar13 = iVar13 + -1;
      } while (iVar13 != 0);
    }
    *(int *)(lVar7 + 0x14) = iVar13;
  }
  return lVar7;
}

undefined8 *FUN_140007050(undefined8 *param_1, uint param_2)

{
  uint uVar1;
  undefined8 *puVar2;
  uint uVar3;
  undefined8 *puVar4;

  if (((param_2 & 3) == 0) ||
      (param_1 = FUN_140006d70(
           param_1,
           *(int *)(&DAT_14000b1a0 + (longlong)(int)((param_2 & 3) - 1) * 4),
           0),
       param_1 != (undefined8 *)0x0)) {
    uVar3 = (int)param_2 >> 2;
    if (uVar3 != 0) {
      puVar2 = DAT_14000e180;
      if (DAT_14000e180 == (undefined8 *)0x0) {
        FUN_140006ae0(1);
        puVar2 = DAT_14000e180;
        if (DAT_14000e180 == (undefined8 *)0x0) {
          puVar2 = (undefined8 *)FUN_140006c10(1);
          if (puVar2 == (undefined8 *)0x0) {
            DAT_14000e180 = (undefined8 *)0x0;
            return (undefined8 *)0x0;
          }
          DAT_14000e180 = puVar2;
          *(undefined8 *)((longlong)puVar2 + 0x14) = 0x27100000001;
          *puVar2 = 0;
        }
        if (DAT_14000eaf0 == 2) {
          LeaveCriticalSection((LPCRITICAL_SECTION)&DAT_14000eb28);
        }
      }
      while (true) {
        puVar4 = puVar2;
        uVar1 = uVar3 & 1;
        uVar3 = (int)uVar3 >> 1;
        if (uVar1 != 0) {
          puVar2 =
              (undefined8 *)FUN_140006ef0((longlong)param_1, (longlong)puVar4);
          if (puVar2 == (undefined8 *)0x0)
            goto LAB_140007143;
          FUN_140006d00(param_1);
          param_1 = puVar2;
        }
        if (uVar3 == 0)
          break;
        puVar2 = (undefined8 *)*puVar4;
        if ((undefined8 *)*puVar4 == (undefined8 *)0x0) {
          FUN_140006ae0(1);
          puVar2 = (undefined8 *)*puVar4;
          if (puVar2 == (undefined8 *)0x0) {
            puVar2 =
                (undefined8 *)FUN_140006ef0((longlong)puVar4, (longlong)puVar4);
            *puVar4 = puVar2;
            if (puVar2 == (undefined8 *)0x0)
              goto LAB_140007143;
            *puVar2 = 0;
          }
          if (DAT_14000eaf0 == 2) {
            LeaveCriticalSection((LPCRITICAL_SECTION)&DAT_14000eb28);
          }
        }
      }
    }
  } else {
  LAB_140007143:
    param_1 = (undefined8 *)0x0;
  }
  return param_1;
}

longlong FUN_1400071d0(undefined8 *param_1, uint param_2)

{
  uint *puVar1;
  int iVar2;
  uint uVar3;
  byte bVar4;
  sbyte sVar5;
  longlong lVar6;
  longlong lVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  uint uVar11;
  uint *puVar12;
  uint *puVar13;
  uint *puVar14;
  uint *puVar15;

  iVar8 = *(int *)(param_1 + 1);
  uVar11 = (int)param_2 >> 5;
  iVar9 = *(int *)((longlong)param_1 + 0x14) + uVar11;
  iVar10 = iVar9 + 1;
  for (iVar2 = *(int *)((longlong)param_1 + 0xc); iVar2 < iVar10;
       iVar2 = iVar2 * 2) {
    iVar8 = iVar8 + 1;
  }
  lVar6 = FUN_140006c10(iVar8);
  if (lVar6 == 0) {
    return 0;
  }
  puVar1 = (uint *)(lVar6 + 0x18);
  puVar14 = puVar1;
  if (0 < (int)uVar11) {
    puVar14 = puVar1 + uVar11;
    memset(puVar1, 0, (ulonglong)uVar11 * 4);
  }
  puVar13 = (uint *)(param_1 + 3);
  puVar1 = puVar13 + *(int *)((longlong)param_1 + 0x14);
  if ((param_2 & 0x1f) == 0) {
    do {
      puVar12 = puVar14 + 1;
      puVar15 = puVar13 + 1;
      *puVar14 = *puVar13;
      if (puVar1 <= puVar15)
        break;
      puVar14 = puVar14 + 2;
      puVar13 = puVar13 + 2;
      *puVar12 = *puVar15;
    } while (puVar13 < puVar1);
  } else {
    uVar11 = 0;
    sVar5 = (sbyte)(param_2 & 0x1f);
    puVar15 = puVar14;
    do {
      puVar12 = puVar13 + 1;
      *puVar15 = *puVar13 << sVar5 | uVar11;
      uVar3 = *puVar13;
      bVar4 = 0x20U - sVar5 & 0x1f;
      uVar11 = uVar3 >> bVar4;
      puVar13 = puVar12;
      puVar15 = puVar15 + 1;
    } while (puVar12 < puVar1);
    lVar7 =
        ((longlong)puVar1 + (-0x19 - (longlong)param_1) & 0xfffffffffffffffcU) +
        4;
    if (puVar1 < (uint *)((longlong)param_1 + 0x19U)) {
      lVar7 = 4;
    }
    *(uint *)((longlong)puVar14 + lVar7) = uVar11;
    if (uVar3 >> bVar4 != 0)
      goto LAB_1400072b2;
  }
  iVar10 = iVar9;
LAB_1400072b2:
  *(int *)(lVar6 + 0x14) = iVar10;
  FUN_140006d00(param_1);
  return lVar6;
}

uint FUN_1400072e0(longlong param_1, longlong param_2)

{
  int iVar1;
  uint *puVar2;
  uint *puVar3;
  uint uVar4;

  iVar1 = *(int *)(param_2 + 0x14);
  uVar4 = *(int *)(param_1 + 0x14) - iVar1;
  if (uVar4 == 0) {
    puVar2 = (uint *)(param_1 + 0x18) + iVar1;
    puVar3 = (uint *)(param_2 + 0x18 + (longlong)iVar1 * 4);
    do {
      puVar2 = puVar2 + -1;
      puVar3 = puVar3 + -1;
      if (*puVar2 != *puVar3) {
        return -(uint)(*puVar2 < *puVar3) | 1;
      }
    } while ((uint *)(param_1 + 0x18) < puVar2);
  }
  return uVar4;
}

longlong FUN_140007330(longlong param_1, longlong param_2)

{
  int *piVar1;
  uint uVar2;
  int iVar3;
  uint *puVar4;
  longlong lVar5;
  ulonglong uVar6;
  longlong lVar7;
  longlong lVar8;
  longlong lVar9;
  uint *puVar10;
  uint *puVar11;
  ulonglong uVar12;
  undefined4 uVar13;
  int *piVar14;
  uint uVar15;
  ulonglong uVar16;
  bool bVar17;

  iVar3 = *(int *)(param_2 + 0x14);
  lVar8 = param_1;
  if (*(int *)(param_1 + 0x14) == iVar3) {
    puVar4 = (uint *)(param_1 + 0x18U) + iVar3;
    puVar11 = (uint *)(param_2 + 0x18 + (longlong)iVar3 * 4);
    do {
      puVar4 = puVar4 + -1;
      puVar11 = puVar11 + -1;
      if (*puVar4 != *puVar11) {
        uVar13 = 1;
        if (*puVar11 <= *puVar4)
          goto LAB_14000738e;
        goto LAB_140007399;
      }
    } while ((uint *)(param_1 + 0x18U) < puVar4);
    lVar5 = FUN_140006c10(0);
    if (lVar5 != 0) {
      *(undefined8 *)(lVar5 + 0x14) = 1;
      return lVar5;
    }
  } else {
    uVar13 = 1;
    if (-1 < *(int *)(param_1 + 0x14) - iVar3) {
    LAB_14000738e:
      uVar13 = 0;
      lVar8 = param_2;
      param_2 = param_1;
    }
  LAB_140007399:
    lVar5 = FUN_140006c10(*(int *)(param_2 + 8));
    if (lVar5 != 0) {
      *(undefined4 *)(lVar5 + 0x10) = uVar13;
      uVar15 = *(uint *)(param_2 + 0x14);
      uVar6 = (ulonglong)(int)uVar15;
      lVar9 = 0x18;
      uVar12 = 0;
      puVar4 = (uint *)(param_2 + 0x18 + uVar6 * 4);
      uVar16 = lVar8 + 0x18 + (longlong) * (int *)(lVar8 + 0x14) * 4;
      do {
        lVar7 = ((ulonglong) * (uint *)(param_2 + lVar9) -
                 (ulonglong) * (uint *)(lVar8 + lVar9)) -
                uVar12;
        iVar3 = (int)lVar7;
        *(int *)(lVar5 + lVar9) = iVar3;
        lVar9 = lVar9 + 4;
        uVar12 = (ulonglong)((uint)((ulonglong)lVar7 >> 0x20) & 1);
      } while ((ulonglong)(lVar9 + lVar8) < uVar16);
      bVar17 = uVar16 < lVar8 + 0x19U;
      uVar16 = (uVar16 - lVar8) - 0x19 >> 2;
      lVar8 = uVar16 * 4 + 4;
      if (bVar17) {
        lVar8 = 4;
      }
      puVar11 = (uint *)(param_2 + 0x18 + lVar8);
      piVar1 = (int *)(lVar5 + 0x18 + lVar8);
      puVar10 = puVar11;
      piVar14 = piVar1;
      if (puVar11 < puVar4) {
        do {
          uVar2 = *puVar10;
          puVar10 = puVar10 + 1;
          iVar3 = (int)(uVar2 - uVar12);
          *piVar14 = iVar3;
          uVar12 = (ulonglong)((uint)(uVar2 - uVar12 >> 0x20) & 1);
          piVar14 = piVar14 + 1;
        } while (puVar10 < puVar4);
        lVar8 =
            (longlong)piVar1 +
            ((longlong)puVar4 + (-1 - (longlong)puVar11) & 0xfffffffffffffffcU);
      } else {
        lVar8 = uVar16 << 2;
        if (bVar17) {
          lVar8 = 0;
        }
        lVar8 = lVar5 + 0x18 + lVar8;
      }
      while (iVar3 == 0) {
        piVar1 = (int *)(lVar8 + -4);
        lVar8 = lVar8 + -4;
        uVar15 = (int)uVar6 - 1;
        uVar6 = (ulonglong)uVar15;
        iVar3 = *piVar1;
      }
      *(uint *)(lVar5 + 0x14) = uVar15;
    }
  }
  return lVar5;
}

ulonglong FUN_140007510(longlong param_1, int *param_2)

{
  ulonglong uVar1;
  longlong lVar2;
  uint uVar3;
  byte bVar4;
  uint uVar5;
  ulonglong uVar6;
  uint uVar7;

  uVar1 = param_1 + 0x18;
  lVar2 = uVar1 + (longlong) * (int *)(param_1 + 0x14) * 4;
  uVar3 = *(uint *)(lVar2 + -4);
  uVar7 = 0x1f;
  if (uVar3 != 0) {
    for (; uVar3 >> uVar7 == 0; uVar7 = uVar7 - 1) {
    }
  }
  uVar7 = uVar7 ^ 0x1f;
  *param_2 = 0x20 - uVar7;
  if (10 < (int)uVar7) {
    bVar4 = (byte)(uVar7 - 0xb);
    if (uVar1 < lVar2 - 4U) {
      uVar5 = *(uint *)(lVar2 + -8);
      uVar6 = (ulonglong)uVar5;
      if (uVar7 - 0xb != 0) {
        uVar3 = uVar3 << (bVar4 & 0x1f) | uVar5 >> (0x20 - bVar4 & 0x1f);
        uVar5 = uVar5 << (bVar4 & 0x1f);
        uVar6 = (ulonglong)uVar5;
        if (uVar1 < lVar2 - 8U) {
          return CONCAT44(uVar3, uVar5 | *(uint *)(lVar2 + -0xc) >>
                                             (0x20 - bVar4 & 0x1f)) |
                 0x3ff0000000000000;
        }
      }
    } else {
      uVar6 = 0;
      if (uVar7 != 0xb) {
        return (ulonglong)(uVar3 << (bVar4 & 0x1f) | 0x3ff00000) << 0x20;
      }
    }
    return (ulonglong)(uVar3 | 0x3ff00000) << 0x20 | uVar6;
  }
  uVar5 = 0;
  bVar4 = 0xb - (char)uVar7;
  if (uVar1 < lVar2 - 4U) {
    uVar5 = *(uint *)(lVar2 + -8) >> (bVar4 & 0x1f);
  }
  return CONCAT44(uVar3 >> (bVar4 & 0x1f),
                  uVar3 << ((char)uVar7 + 0x15U & 0x1f) | uVar5) |
         0x3ff0000000000000;
}

ulonglong FUN_140007770(char *param_1, ulonglong param_2)

{
  char *pcVar1;
  ulonglong uVar2;

  uVar2 = 0;
  pcVar1 = param_1;
  if (param_2 != 0) {
    do {
      if (*pcVar1 == '\0') {
        return uVar2;
      }
      pcVar1 = pcVar1 + 1;
      uVar2 = (longlong)pcVar1 - (longlong)param_1;
    } while (uVar2 < param_2);
  }
  return uVar2;
}

longlong FUN_1400077a0(longlong param_1, longlong param_2)

{
  longlong lVar1;

  lVar1 = 0;
  if (param_2 != 0) {
    do {
      if (*(short *)(param_1 + lVar1 * 2) == 0) {
        return param_2;
      }
      lVar1 = lVar1 + 1;
    } while (param_2 != lVar1);
  }
  return param_2;
}

undefined *FUN_1400077d0(void)

{
  return _fmode_exref;
}

undefined *FUN_1400077e0(void)

{
  return _commode_exref;
}

void FUN_1400077f0(FILE *param_1)

{
  FILE *pFVar1;

  pFVar1 = FUN_1400078e0(0);
  if (pFVar1 <= param_1) {
    pFVar1 = FUN_1400078e0(0x13);
    if (param_1 <= pFVar1) {
      pFVar1 = FUN_1400078e0(0);
      _lock((int)((longlong)param_1 - (longlong)pFVar1 >> 4) * -0x55555555 +
            0x10);
      param_1->_flag = param_1->_flag | 0x8000;
      return;
    }
  }
  // WARNING: Could not recover jumptable at 0x00014000781c. Too many branches
  // WARNING: Treating indirect jump as call
  EnterCriticalSection((LPCRITICAL_SECTION)(param_1 + 1));
  return;
}

void FUN_140007860(FILE *param_1)

{
  FILE *pFVar1;

  pFVar1 = FUN_1400078e0(0);
  if (pFVar1 <= param_1) {
    pFVar1 = FUN_1400078e0(0x13);
    if (param_1 <= pFVar1) {
      param_1->_flag = param_1->_flag & 0xffff7fff;
      pFVar1 = FUN_1400078e0(0);
      _unlock((int)((longlong)param_1 - (longlong)pFVar1 >> 4) * -0x55555555 +
              0x10);
      return;
    }
  }
  // WARNING: Could not recover jumptable at 0x00014000788c. Too many branches
  // WARNING: Treating indirect jump as call
  LeaveCriticalSection((LPCRITICAL_SECTION)(param_1 + 1));
  return;
}

undefined8 FUN_1400078d0(undefined8 param_1)

{
  undefined8 uVar1;

  uVar1 = DAT_14000eb60;
  LOCK();
  DAT_14000eb60 = param_1;
  UNLOCK();
  return uVar1;
}

FILE *FUN_1400078e0(uint param_1)

{
  FILE *pFVar1;

  pFVar1 = __iob_func();
  return pFVar1 + param_1;
}

int FUN_140007900(LPSTR param_1, WCHAR param_2, UINT param_3, int param_4)

{
  int iVar1;
  int *piVar2;
  WCHAR local_res10[12];
  BOOL local_c[3];

  local_res10[0] = param_2;
  if (param_3 == 0) {
    if (0xff < (ushort)param_2) {
    LAB_140007974:
      piVar2 = _errno();
      *piVar2 = 0x2a;
      return -1;
    }
    *param_1 = (CHAR)param_2;
    iVar1 = 1;
  } else {
    local_c[0] = 0;
    iVar1 = WideCharToMultiByte(param_3, 0, local_res10, 1, param_1, param_4,
                                (LPCSTR)0x0, local_c);
    if ((iVar1 == 0) || (local_c[0] != 0))
      goto LAB_140007974;
  }
  return iVar1;
}

longlong FUN_140007990(LPSTR param_1, WCHAR param_2)

{
  int iVar1;
  UINT UVar2;
  CHAR local_1d[5];

  if (param_1 == (LPSTR)0x0) {
    param_1 = local_1d;
  }
  iVar1 = ___mb_cur_max_func();
  UVar2 = ___lc_codepage_func();
  iVar1 = FUN_140007900(param_1, param_2, UVar2, iVar1);
  return (longlong)iVar1;
}

undefined8 FUN_140007ad0(LPWSTR param_1, byte *param_2, longlong param_3,
                         byte *param_4, UINT param_5, uint param_6)

{
  byte TestChar;
  uint uVar1;
  char cVar2;
  BOOL BVar3;
  int iVar4;
  int *piVar5;
  undefined4 local_1c;

  if (param_2 == (byte *)0x0) {
    return 0;
  }
  if (param_3 == 0) {
    return 0xfffffffe;
  }
  local_1c = *(undefined4 *)param_4;
  TestChar = *param_2;
  param_4[0] = 0;
  param_4[1] = 0;
  param_4[2] = 0;
  param_4[3] = 0;
  if (TestChar == 0) {
    *param_1 = L'\0';
    return 0;
  }
  if (param_6 < 2) {
  LAB_140007b88:
    if (param_5 == 0) {
      *param_1 = (ushort)*param_2;
      return 1;
    }
    iVar4 = MultiByteToWideChar(param_5, 8, (LPCSTR)param_2, 1, param_1, 1);
    if (iVar4 != 0) {
      return 1;
    }
  } else {
    cVar2 = (char)local_1c;
    if (cVar2 == '\0') {
      BVar3 = IsDBCSLeadByteEx(param_5, TestChar);
      if (BVar3 == 0)
        goto LAB_140007b88;
      if (param_3 == 1) {
        *param_4 = *param_2;
        return 0xfffffffe;
      }
    } else {
      uVar1 = (uint)local_1c >> 0x10;
      local_1c._2_2_ = (undefined2)uVar1;
      local_1c._0_2_ = CONCAT11(TestChar, cVar2);
      param_2 = (byte *)&local_1c;
    }
    iVar4 = MultiByteToWideChar(param_5, 8, (LPCSTR)param_2, 2, param_1, 1);
    if (iVar4 != 0) {
      return 2;
    }
  }
  piVar5 = _errno();
  *piVar5 = 0x2a;
  return 0xffffffff;
}

longlong FUN_140007c30(LPWSTR param_1, byte *param_2, longlong param_3,
                       byte *param_4)

{
  uint uVar1;
  UINT UVar2;
  undefined8 uVar3;
  byte *pbVar4;
  WCHAR local_2a;

  local_2a = L'\0';
  if (param_1 == (LPWSTR)0x0) {
    param_1 = &local_2a;
  }
  uVar1 = ___mb_cur_max_func();
  UVar2 = ___lc_codepage_func();
  pbVar4 = &DAT_14000eb78;
  if (param_4 != (byte *)0x0) {
    pbVar4 = param_4;
  }
  uVar3 = FUN_140007ad0(param_1, param_2, param_3, pbVar4, UVar2, uVar1);
  return (longlong)(int)uVar3;
}

UINT __cdecl ___lc_codepage_func(void)

{
  UINT UVar1;

  // WARNING: Could not recover jumptable at 0x000140007e18. Too many branches
  // WARNING: Treating indirect jump as call
  UVar1 = ___lc_codepage_func();
  return UVar1;
}

int __cdecl ___mb_cur_max_func(void)

{
  int iVar1;

  // WARNING: Could not recover jumptable at 0x000140007e20. Too many branches
  // WARNING: Treating indirect jump as call
  iVar1 = ___mb_cur_max_func();
  return iVar1;
}

void __getmainargs(void)

{
  // WARNING: Could not recover jumptable at 0x000140007e28. Too many branches
  // WARNING: Treating indirect jump as call
  __getmainargs();
  return;
}

FILE *__cdecl __iob_func(void)

{
  FILE *pFVar1;

  // WARNING: Could not recover jumptable at 0x000140007e30. Too many branches
  // WARNING: Treating indirect jump as call
  pFVar1 = __iob_func();
  return pFVar1;
}

void __cdecl __set_app_type(int param_1)

{
  // WARNING: Could not recover jumptable at 0x000140007e38. Too many branches
  // WARNING: Treating indirect jump as call
  __set_app_type(param_1);
  return;
}

void __setusermatherr(void)

{
  // WARNING: Could not recover jumptable at 0x000140007e40. Too many branches
  // WARNING: Treating indirect jump as call
  __setusermatherr();
  return;
}

void __cdecl _amsg_exit(int param_1)

{
  // WARNING: Could not recover jumptable at 0x000140007e48. Too many branches
  // WARNING: Treating indirect jump as call
  _amsg_exit(param_1);
  return;
}

void __cdecl _cexit(void)

{
  // WARNING: Could not recover jumptable at 0x000140007e50. Too many branches
  // WARNING: Treating indirect jump as call
  _cexit();
  return;
}

int *__cdecl _errno(void)

{
  int *piVar1;

  // WARNING: Could not recover jumptable at 0x000140007e58. Too many branches
  // WARNING: Treating indirect jump as call
  piVar1 = _errno();
  return piVar1;
}

void _initterm(void)

{
  // WARNING: Could not recover jumptable at 0x000140007e68. Too many branches
  // WARNING: Treating indirect jump as call
  _initterm();
  return;
}

void __cdecl _lock(int _File)

{
  // WARNING: Could not recover jumptable at 0x000140007e70. Too many branches
  // WARNING: Treating indirect jump as call
  _lock(_File);
  return;
}

_onexit_t __cdecl _onexit(_onexit_t _Func)

{
  _onexit_t p_Var1;

  // WARNING: Could not recover jumptable at 0x000140007e78. Too many branches
  // WARNING: Treating indirect jump as call
  p_Var1 = _onexit(_Func);
  return p_Var1;
}

void __cdecl _unlock(int _File)

{
  // WARNING: Could not recover jumptable at 0x000140007e80. Too many branches
  // WARNING: Treating indirect jump as call
  _unlock(_File);
  return;
}

void __cdecl abort(void)

{
  // WARNING: Could not recover jumptable at 0x000140007e88. Too many branches
  // WARNING: Subroutine does not return
  // WARNING: Treating indirect jump as call
  abort();
  return;
}

void *__cdecl calloc(size_t _Count, size_t _Size)

{
  void *pvVar1;

  // WARNING: Could not recover jumptable at 0x000140007e90. Too many branches
  // WARNING: Treating indirect jump as call
  pvVar1 = calloc(_Count, _Size);
  return pvVar1;
}

void __cdecl exit(int _Code)

{
  // WARNING: Could not recover jumptable at 0x000140007e98. Too many branches
  // WARNING: Subroutine does not return
  // WARNING: Treating indirect jump as call
  exit(_Code);
  return;
}

int __cdecl fclose(FILE *_File)

{
  int iVar1;

  // WARNING: Could not recover jumptable at 0x000140007ea0. Too many branches
  // WARNING: Treating indirect jump as call
  iVar1 = fclose(_File);
  return iVar1;
}

FILE *__cdecl fopen(char *_Filename, char *_Mode)

{
  FILE *pFVar1;

  // WARNING: Could not recover jumptable at 0x000140007ea8. Too many branches
  // WARNING: Treating indirect jump as call
  pFVar1 = fopen(_Filename, _Mode);
  return pFVar1;
}

int __cdecl fprintf(FILE *_File, char *_Format, ...)

{
  int iVar1;

  // WARNING: Could not recover jumptable at 0x000140007eb0. Too many branches
  // WARNING: Treating indirect jump as call
  iVar1 = fprintf(_File, _Format);
  return iVar1;
}

int __cdecl fputc(int _Ch, FILE *_File)

{
  int iVar1;

  // WARNING: Could not recover jumptable at 0x000140007eb8. Too many branches
  // WARNING: Treating indirect jump as call
  iVar1 = fputc(_Ch, _File);
  return iVar1;
}

size_t __cdecl fread(void *_DstBuf, size_t _ElementSize, size_t _Count,
                     FILE *_File)

{
  size_t sVar1;

  // WARNING: Could not recover jumptable at 0x000140007ec0. Too many branches
  // WARNING: Treating indirect jump as call
  sVar1 = fread(_DstBuf, _ElementSize, _Count, _File);
  return sVar1;
}

void __cdecl free(void *_Memory)

{
  // WARNING: Could not recover jumptable at 0x000140007ec8. Too many branches
  // WARNING: Treating indirect jump as call
  free(_Memory);
  return;
}

int __cdecl fseek(FILE *_File, long _Offset, int _Origin)

{
  int iVar1;

  // WARNING: Could not recover jumptable at 0x000140007ed0. Too many branches
  // WARNING: Treating indirect jump as call
  iVar1 = fseek(_File, _Offset, _Origin);
  return iVar1;
}

long __cdecl ftell(FILE *_File)

{
  long lVar1;

  // WARNING: Could not recover jumptable at 0x000140007ed8. Too many branches
  // WARNING: Treating indirect jump as call
  lVar1 = ftell(_File);
  return lVar1;
}

size_t __cdecl fwrite(void *_Str, size_t _Size, size_t _Count, FILE *_File)

{
  size_t sVar1;

  // WARNING: Could not recover jumptable at 0x000140007ee0. Too many branches
  // WARNING: Treating indirect jump as call
  sVar1 = fwrite(_Str, _Size, _Count, _File);
  return sVar1;
}

lconv *__cdecl localeconv(void)

{
  lconv *plVar1;

  // WARNING: Could not recover jumptable at 0x000140007ee8. Too many branches
  // WARNING: Treating indirect jump as call
  plVar1 = localeconv();
  return plVar1;
}

void *__cdecl malloc(size_t _Size)

{
  void *pvVar1;

  // WARNING: Could not recover jumptable at 0x000140007ef0. Too many branches
  // WARNING: Treating indirect jump as call
  pvVar1 = malloc(_Size);
  return pvVar1;
}

void *__cdecl memcpy(void *_Dst, void *_Src, size_t _Size)

{
  void *pvVar1;

  // WARNING: Could not recover jumptable at 0x000140007ef8. Too many branches
  // WARNING: Treating indirect jump as call
  pvVar1 = memcpy(_Dst, _Src, _Size);
  return pvVar1;
}

void *__cdecl memset(void *_Dst, int _Val, size_t _Size)

{
  void *pvVar1;

  // WARNING: Could not recover jumptable at 0x000140007f00. Too many branches
  // WARNING: Treating indirect jump as call
  pvVar1 = memset(_Dst, _Val, _Size);
  return pvVar1;
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

void signal(int param_1)

{
  // WARNING: Could not recover jumptable at 0x000140007f08. Too many branches
  // WARNING: Treating indirect jump as call
  signal(param_1);
  return;
}

char *__cdecl strerror(int param_1)

{
  char *pcVar1;

  // WARNING: Could not recover jumptable at 0x000140007f10. Too many branches
  // WARNING: Treating indirect jump as call
  pcVar1 = strerror(param_1);
  return pcVar1;
}

size_t __cdecl strlen(char *_Str)

{
  size_t sVar1;

  // WARNING: Could not recover jumptable at 0x000140007f18. Too many branches
  // WARNING: Treating indirect jump as call
  sVar1 = strlen(_Str);
  return sVar1;
}

int __cdecl strncmp(char *_Str1, char *_Str2, size_t _MaxCount)

{
  int iVar1;

  // WARNING: Could not recover jumptable at 0x000140007f20. Too many branches
  // WARNING: Treating indirect jump as call
  iVar1 = strncmp(_Str1, _Str2, _MaxCount);
  return iVar1;
}

int __cdecl vfprintf(FILE *_File, char *_Format, va_list _ArgList)

{
  int iVar1;

  // WARNING: Could not recover jumptable at 0x000140007f28. Too many branches
  // WARNING: Treating indirect jump as call
  iVar1 = vfprintf(_File, _Format, _ArgList);
  return iVar1;
}

size_t __cdecl wcslen(wchar_t *_Str)

{
  size_t sVar1;

  // WARNING: Could not recover jumptable at 0x000140007f30. Too many branches
  // WARNING: Treating indirect jump as call
  sVar1 = wcslen(_Str);
  return sVar1;
}
