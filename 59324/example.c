#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <assert.h>

struct flags {
  unsigned long a: 42;
  unsigned int b: 7;
};

int main(void) {
  struct flags my_flags;
  assert(sizeof(struct flags) == 8);
  assert(sizeof(unsigned long) == 8);
  
  unsigned char buffer[1000];

  /* Set a to all 1s. */
//   my_flags.a = 4398046511103U;
  my_flags.a = -1;
  memcpy(buffer, &my_flags, sizeof(my_flags));
  write(1, buffer, sizeof(my_flags));
  my_flags.a = 0;

  /* Set b to all 1s. */
//   my_flags.b = 127U;
  my_flags.b = -1;
  memcpy(buffer, &my_flags, sizeof(my_flags));
  write(1, buffer, sizeof(my_flags));
  my_flags.b = 0;

  return 0;
}
